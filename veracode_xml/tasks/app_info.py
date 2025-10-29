"""
Fetch information for a specific application.
Reference: https://docs.veracode.com/r/r_getappinfo
"""

import argparse
import sys
import requests
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC
from veracode_xml.utils.api_helpers import find_app_by_name, save_output, pretty_print_xml
from veracode_xml.config import endpoint_getappinfo

HELP_TEXT = "Fetch detailed info for a specific Veracode application by app_id."

def setup_parser(parser: argparse.ArgumentParser):
    parser.add_argument(
        "-a", "--app_id",
        help="Application ID (integer) (alternate to --app_name). Example: 2477056"
    )
    parser.add_argument(
        "-n", "--app_name",
        help="Veracode application name (alternate to --app_id). Example: verademo"
    )
    parser.add_argument(
        "-r", "--region",
        default="us",
        choices=["us", "eu", "us_fed"],
        help="Region for Veracode platform (default: us)."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Print full XML response."
    )



def run(args):
    import sys
    import requests
    from veracode_xml.config import xml_api_v5_base

    url = xml_api_v5_base(args.region) + "getappinfo.do"
    params = {"app_id": args.app_id}

    print(f"📡 Fetching app info for app_id={args.app_id} ...")
    resp = requests.get(url, params=params, auth=requests.auth.HTTPDigestAuth(
        # expects ~/.veracode/credentials or env vars
        os.getenv("VERACODE_API_ID"),
        os.getenv("VERACODE_API_KEY")
    ))

    if resp.status_code != 200:
        print(f"❌ API request failed ({resp.status_code}): {resp.text}")
        sys.exit(1)

    if args.verbose:
        print(resp.text)

    # Parse XML with namespaces
    root = ET.fromstring(resp.text)
    ns = {"ns": "https://analysiscenter.veracode.com/schema/2.0/appinfo"}

    app_elem = root.find("ns:application", ns)
    if app_elem is None:
        print("⚠️  No <application> element found — response may be malformed.")
        sys.exit(1)

    # Extract details
    app_info = {
        "app_id": app_elem.attrib.get("app_id"),
        "app_name": app_elem.attrib.get("app_name"),
        "business_criticality": app_elem.attrib.get("business_criticality"),
        "policy": app_elem.attrib.get("policy"),
        "policy_updated_date": app_elem.attrib.get("policy_updated_date"),
        "teams": app_elem.attrib.get("teams"),
        "business_unit": app_elem.attrib.get("business_unit"),
        "modified_date": app_elem.attrib.get("modified_date"),
    }

    print("\n✅ Application Info:")
    for k, v in app_info.items():
        print(f"  {k:22} : {v or '-'}")

    # Optional: print custom fields
    custom_fields = app_elem.findall("ns:customfield", ns)
    if custom_fields:
        print("\n🧩 Custom Fields:")
        for cf in custom_fields:
            print(f"  {cf.attrib['name']}: {cf.attrib.get('value', '') or '-'}")
