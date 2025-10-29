"""
List all builds under a given application.
Reference: https://docs.veracode.com/r/r_getbuildlist
"""

import xml.etree.ElementTree as ET
import requests
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC
from veracode_xml.config import endpoint_getbuildlist

HELP_TEXT = "List all builds under a specific application."

def setup_parser(parser):
    parser.add_argument("-a", "--app_id", required=True, help="Veracode application ID")
    parser.add_argument("-r", "--region", default="us", help="Veracode region (us, eu, us_fed)")

def run(args):
    url = endpoint_getbuildlist(args.region) + f"?app_id={args.app_id}"
    print(f"📡 Fetching builds for app_id={args.app_id} ...")

    response = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC())
    if response.status_code != 200:
        print(f"❌ API request failed: {response.status_code}")
        print(response.text)
        return

    try:
        root = ET.fromstring(response.text)
        ns = {"ns": root.tag.split('}')[0].strip('{')} if "}" in root.tag else {}

        builds = root.findall(".//ns:build", ns) or root.findall(".//build")
        if not builds:
            print("⚠️  No builds found for this app.")
            return

        print(f"✅ Found {len(builds)} builds:\n")
        for b in builds:
            print(
                f"• Build ID: {b.attrib.get('build_id')}, "
                f"Version: {b.attrib.get('version')}, "
                f"Scan Type: {'Dynamic' if b.attrib.get('dynamic_scan_type') else 'Static'}"
            )

    except ET.ParseError as e:
        print(f"❌ Failed to parse XML: {e}")
