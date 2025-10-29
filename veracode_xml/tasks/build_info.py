"""
Fetch detailed build information.
Reference: https://docs.veracode.com/r/r_getbuildinfo
If build_id is not given, fetches the latest build (based on scan_type).
"""

import xml.etree.ElementTree as ET
import requests
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC
from veracode_xml.config import endpoint_getbuildinfo, endpoint_getbuildlist

HELP_TEXT = "Fetch info for a specific or latest build."

def setup_parser(parser):
    parser.add_argument("-a", "--app_id", help="Veracode application ID")
    parser.add_argument("-b", "--build_id", help="Specific build ID (optional)")
    parser.add_argument(
        "-s", "--scan_type", choices=["ss", "ds"], default="ss",
        help="Scan type: ss=Static, ds=Dynamic (used if build_id not given)"
    )
    parser.add_argument("-r", "--region", default="us", help="Veracode region (us, eu, us_fed)")

def run(args):
    if not args.app_id and not args.build_id:
        print("❌ app_id is required when build_id is not provided.")
        return

    build_id = args.build_id
    if not build_id:
        # Fetch latest build ID first
        list_url = endpoint_getbuildlist(args.region) + f"?app_id={args.app_id}"
        resp = requests.get(list_url, auth=RequestsAuthPluginVeracodeHMAC())
        if resp.status_code != 200:
            print(f"❌ Failed to fetch build list: {resp.status_code}")
            print(resp.text)
            return

        root = ET.fromstring(resp.text)
        ns = {"ns": root.tag.split('}')[0].strip('{')} if "}" in root.tag else {}
        builds = root.findall(".//ns:build", ns) or root.findall(".//build")

        if not builds:
            print("⚠️  No builds found for this app.")
            return

        # Pick the latest matching scan type
        filtered = [b for b in builds if b.attrib.get("dynamic_scan_type", "ss") == args.scan_type]
        if not filtered:
            print(f"⚠️  No builds found for scan_type={args.scan_type.upper()}.")
            return

        latest = filtered[-1]  # assuming API returns in order
        build_id = latest.attrib["build_id"]
        print(f"🔍 Using latest build_id={build_id} (scan_type={args.scan_type})")

    # Fetch build info
    url = endpoint_getbuildinfo(args.region) + f"?app_id={args.app_id}&build_id={build_id}"
    print(f"📡 Fetching build info for build_id={build_id} ...")

    response = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC())
    if response.status_code != 200:
        print(f"❌ API request failed: {response.status_code}")
        print(response.text)
        return

    try:
        root = ET.fromstring(response.text)
        ns = {"ns": root.tag.split('}')[0].strip('{')} if "}" in root.tag else {}
        build = root.find(".//ns:build", ns) or root.find(".//build")
        if build is None:
            print("⚠️  No build info found.")
            return

        print("✅ Build Info:")
        for k, v in build.attrib.items():
            print(f"  {k}: {v}")

    except ET.ParseError as e:
        print(f"❌ Failed to parse XML: {e}")
