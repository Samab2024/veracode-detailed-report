import sys
import requests
import xml.etree.ElementTree as ET
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC
from veracode_xml.config import get_api_base

HELP_TEXT = "📋 List all applications in your Veracode account"

def setup_parser(parser):
    parser.add_argument(
        "-r", "--region",
        choices=["us", "eu", "gov"],
        default="us",
        help="Region to use (default: us)"
    )

def run(args):
    api_base = get_api_base(args.region)
    url = f"{api_base}/api/5.0/getapplist.do"

    try:
        response = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC())
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Failed to fetch app list:\n{e}")
        sys.exit(1)

    root = ET.fromstring(response.text)
    ns = {"ns": "https://analysiscenter.veracode.com/schema/5.0/applist"}

    apps = root.findall(".//ns:app", ns)
    if not apps:
        print("⚠️  No applications found.")
        return

    print(f"✅ Found {len(apps)} applications:\n")
    for app in apps:
        app_id = app.get("app_id")
        app_name = app.get("app_name")
        policy = app.get("policy_name", "N/A")
        print(f" - {app_name} (ID: {app_id}) | Policy: {policy}")
