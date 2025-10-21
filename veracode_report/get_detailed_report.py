#!/usr/bin/env python3
"""
Veracode Detailed Report Fetcher

Fetches Veracode Detailed Reports (XML or PDF) using HMAC authentication.
Supports both app_id and app_name, and allows selecting region (US/EU).
"""

import sys
import os
import argparse
import xml.etree.ElementTree as ET
import requests
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC

# Default User-Agent
HEADERS = {"User-Agent": "Veracode Detailed Report Fetcher"}

# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------

def get_api_base(region: str) -> str:
    """Return API base URL for selected region."""
    if region.lower() == "eu":
        return "https://analysiscenter.veracode.eu"
    return "https://analysiscenter.veracode.com"


def get_app_id_from_name(api_base: str, app_name: str) -> str:
    """Look up app_id from app_name."""
    url = f"{api_base}/api/5.0/getapplist.do"
    print(f"🔍 Looking up app_id for app_name='{app_name}' ...")
    try:
        response = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC(), headers=HEADERS)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Failed to fetch app list: {e}")
        sys.exit(1)

    try:
        root = ET.fromstring(response.text)
        for app in root.findall(".//app"):
            if app.get("app_name") == app_name:
                app_id = app.get("app_id")
                print(f"✅ Found app_id={app_id}")
                return app_id
        print(f"⚠️  Application name '{app_name}' not found in app list.")
        sys.exit(1)
    except ET.ParseError:
        print("❌ Failed to parse XML response while fetching app list.")
        sys.exit(1)


def get_build_id(api_base: str, app_id: str) -> str:
    """Fetch the latest build_id for a given app_id."""
    print(f"\n📦 Fetching build info for app_id={app_id} ...")
    url = f"{api_base}/api/5.0/getbuildinfo.do?app_id={app_id}"

    try:
        response = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC(), headers=HEADERS)
        response.raise_for_status()
        print(f"HTTP Status: {response.status_code}")
    except requests.RequestException as e:
        print(f"❌ Error fetching build info: {e}")
        sys.exit(1)

    # Parse XML response
    try:
        root = ET.fromstring(response.text)
        build_elem = root.find(".//build")
        if build_elem is not None and build_elem.get("build_id"):
            build_id = build_elem.get("build_id")
            print(f"✅ Found build_id={build_id}")
            return build_id
        else:
            print("⚠️  No build_id found in response XML.")
            sys.exit(1)
    except ET.ParseError:
        print("❌ Failed to parse XML from getbuildinfo response.")
        sys.exit(1)


def fetch_detailed_report(api_base: str, build_id: str, report_type: str, output_dir: str, prefix: str):
    """Fetch and save the Veracode detailed report."""
    print(f"\n📥 Fetching {report_type} detailed report for build_id={build_id} ...")

    if report_type.upper() == "PDF":
        endpoint = f"/api/4.0/detailedreportpdf.do?build_id={build_id}"
        extension = "pdf"
    else:
        endpoint = f"/api/5.0/detailedreport.do?build_id={build_id}"
        extension = "xml"

    url = f"{api_base}{endpoint}"

    try:
        response = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC(), headers=HEADERS)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Failed to fetch detailed report: {e}")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)
    filename = f"{prefix}{build_id}.{extension}"
    filepath = os.path.join(output_dir, filename)

    mode = "wb" if extension == "pdf" else "w"
    with open(filepath, mode) as f:
        if extension == "pdf":
            f.write(response.content)
        else:
            f.write(response.text)

    print(f"✅ Report saved to: {filepath}")


# -----------------------------------------------------------------------------
# Main CLI entry point
# -----------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Fetch Veracode Detailed Report (XML or PDF) using app_id or app_name."
    )
    parser.add_argument("app", help="Veracode application ID or name")
    parser.add_argument("report_type", choices=["XML", "PDF"], help="Report type to download")
    parser.add_argument("--region", choices=["us", "eu"], default="us", help="Veracode region (default: us)")
    parser.add_argument("--output_dir", default="./reports", help="Directory to save reports")
    parser.add_argument("--prefix", default="veracode_", help="Filename prefix for saved report")
    args = parser.parse_args()

    api_base = get_api_base(args.region)

    if args.app.isdigit():
        app_id = args.app
    else:
        app_id = get_app_id_from_name(api_base, args.app)

    build_id = get_build_id(api_base, app_id)
    fetch_detailed_report(api_base, build_id, args.report_type, args.output_dir, args.prefix)


if __name__ == "__main__":
    main()
