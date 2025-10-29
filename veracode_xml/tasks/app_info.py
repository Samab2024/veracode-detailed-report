import sys
import requests
import xml.etree.ElementTree as ET
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC
from veracode_xml.config import get_api_base

HELP_TEXT = "📘 Get detailed information for a specific application"

def setup_parser(parser):
    parser.add_argument(
        "-a", "--app_id",
        required=True,
        help="Veracode application ID (required)"
    )
    parser.add_argument(
        "-r", "--region",
        choices=["us", "eu", "gov"],
        default="us",
        help="Region to use (default: us)"
    )

def run(args):
    api_base = get_api_base(args.region)
    url = f"{api_base}/api/5.0/getappinfo.do?app_id={args.app_id}"

    try:
        response = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC())
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Failed to fetch app info:\n{e}")
        sys.exit(1)

    root = ET.fromstring(response.text)
    ns = {"ns": "https://analysiscenter.veracode.com/schema/5.0/appinfo"}

    app = root.find(".//ns:app", ns)
    if app is None:
        print("⚠️  Application not found or invalid response.")
        return

    print("\n✅ Application Info:")
    print(f" - ID: {app.get('app_id')}")
    print(f" - Name: {app.get('app_name')}")
    print(f" - Policy: {app.get('policy_name')}")
    print(f" - Teams: {app.get('business_criticality')}")
    print(f" - Last Modified: {app.get('last_modified_date')}")
