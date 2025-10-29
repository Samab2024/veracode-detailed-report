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

    try:
        root = ET.fromstring(response.text)
        ns = {"ns": root.tag.split('}')[0].strip('{')} if "}" in root.tag else {}

        app = root.find(".//ns:app", ns) or root.find(".//app")
        if app is None:
            print("⚠️  No app info found.")
            return

        print("✅ Application Info:")
        for k, v in app.attrib.items():
            print(f"  {k}: {v}")

    except ET.ParseError as e:
        print(f"❌ Failed to parse XML: {e}")
