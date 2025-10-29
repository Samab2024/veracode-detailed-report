"""
Fetch information for a specific application.
Reference: https://docs.veracode.com/r/r_getappinfo
"""

import xml.etree.ElementTree as ET
import requests
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC
from veracode_xml.config import xml_api_v5_base

HELP_TEXT = "Get detailed info for a specific application."

def setup_parser(parser):
    parser.add_argument("-a", "--app_id", required=True, help="Veracode application ID")
    parser.add_argument("-r", "--region", default="us", help="Veracode region (us, eu, us_fed)")

def run(args):
    url = xml_api_v5_base(args.region) + f"getappinfo.do?app_id={args.app_id}"
    print(f"📡 Fetching app info for app_id={args.app_id} ...")

    response = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC())
    if response.status_code != 200:
        print(f"❌ API request failed: {response.status_code}")
        print(response.text)
        return

    # Parse XML with namespaces
    root = ET.fromstring(response.text)
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
