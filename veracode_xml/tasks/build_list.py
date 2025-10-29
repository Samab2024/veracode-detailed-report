"""
List all builds under a given application.
Reference: https://docs.veracode.com/r/r_getbuildlist
"""

import xml.etree.ElementTree as ET
import requests
import sys
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC
from veracode_xml.config import endpoint_getbuildlist, endpoint_getapplist

HELP_TEXT = "🧱 List all builds under a specific application."

def setup_parser(parser):
    parser.add_argument("-a", "--app_id", help="Veracode application ID")
    parser.add_argument("-n", "--app_name", help="Veracode application name (alternate to --app_id)")
    parser.add_argument("-r", "--region", default="us", help="Veracode region (us, eu, us_fed)")

def _resolve_app_id_from_name(app_name: str, region: str = "us") -> str | None:
    """Resolve app_name -> app_id using getapplist.do (namespace-safe)."""
    url = endpoint_getapplist(region)
    resp = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC())
    if resp.status_code != 200:
        print(f"❌ Failed to fetch app list for name resolution: HTTP {resp.status_code}")
        return None
    try:
        root = ET.fromstring(resp.text)
    except ET.ParseError as e:
        print(f"❌ Failed to parse app list XML: {e}")
        return None

    ns = {"ns": root.tag.split('}')[0].strip('{')} if "}" in root.tag else {}
    apps = root.findall(".//ns:app", ns) if ns else root.findall(".//app")
    for app in apps:
        if app.attrib.get("app_name") == app_name:
            return app.attrib.get("app_id")
    return None


def run(args):
    # Resolve app_id from name if needed
    app_id = args.app_id
    if not app_id and args.app_name:
        print(f"Resolving app_id for app_name='{args.app_name}' ...")
        app_id = _resolve_app_id_from_name(args.app_name, args.region)
        if not app_id:
            print(f"❌ App name '{args.app_name}' not found in your Veracode account.")
            return

    if not app_id:
        print("❌ Please provide --app_id or --app_name.")
        return

    url = endpoint_getbuildlist(args.region) + f"?app_id={app_id}"
    print(f"📡 Fetching builds for app_id={app_id} ...")

    response = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC())
    if response.status_code != 200:
        print(f"❌ API request failed: {response.status_code}")
        print(response.text)
        return

    try:
        root = ET.fromstring(response.text)
        ns = {"ns": root.tag.split('}')[0].strip('{')} if "}" in root.tag else {}
        builds = root.findall(".//ns:build", ns) if ns else root.findall(".//build")

        if not builds:
            print("⚠️  No builds found for this app.")
            return

        print(f"✅ Found {len(builds)} builds:\n")
        for b in builds:
            print(
                f"• Build ID: {b.attrib.get('build_id')}, "
                f"Version: {b.attrib.get('version')}, "
                f"Scan Type: {'Dynamic' if b.attrib.get('dynamic_scan_type') else 'Static'}, "
                f"Date: {b.attrib.get('policy_updated_date', 'N/A')}"
            )

    except ET.ParseError as e:
        print(f"❌ Failed to parse XML: {e}")
