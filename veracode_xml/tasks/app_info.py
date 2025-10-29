"""
veracode_xml.tasks.app_info
Fetch detailed information for a specific Veracode application ID via XML API.
"""

import requests
import xml.etree.ElementTree as ET
import sys
from veracode_xml.config import endpoint_getapplist, xml_api_v5_base, DEFAULT_REGION
from veracode_xml.config import endpoint_getbuildinfo, api_base_xml, xml_api_v5_base

HELP_TEXT = "Fetch detailed info for a specific Veracode application (by app_id)."

def setup_parser(parser):
    parser.add_argument(
        "-a", "--app_id",
        required=True,
        help="Application ID to fetch info for."
    )
    parser.add_argument(
        "-r", "--region",
        default=DEFAULT_REGION,
        help="Region code (default: us)."
    )


def run(args):
    url = f"{xml_api_v5_base(args.region)}getappinfo.do"
    params = {"app_id": args.app_id}

    print(f"📡 Fetching app info for app_id={args.app_id} ...")

    try:
        resp = requests.get(url, params=params, auth=requests.auth.HTTPBasicAuth(
            # The Veracode API key credentials are taken from ~/.veracode/credentials
            # or environment variables. If you already have them configured, this works directly.
            os.getenv("VERACODE_API_ID"),
            os.getenv("VERACODE_API_KEY")
        ))

        if resp.status_code != 200:
            print(f"❌ HTTP {resp.status_code}: {resp.text}")
            sys.exit(1)

        root = ET.fromstring(resp.text)

        app_elem = root.find("application")
        if app_elem is None:
            print("⚠️  No <application> element found in XML response.")
            return

        app_id = app_elem.get("app_id")
        app_name = app_elem.get("app_name")
        policy_elem = app_elem.find("profile")

        policy_name = policy_elem.get("policy_name") if policy_elem is not None else "None"

        print(f"\n✅ Application Info:")
        print(f"• Name: {app_name}")
        print(f"• ID:   {app_id}")
        print(f"• Policy: {policy_name}")

    except ET.ParseError:
        print("❌ Failed to parse XML response.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
