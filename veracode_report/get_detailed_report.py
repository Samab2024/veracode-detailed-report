#!/usr/bin/env python3
"""
veracode-detailed-report: Fetch Veracode Detailed Reports (XML/PDF) for Static or Dynamic scans.
Supports app_id or app_name, automatically detects scan type and retrieves latest build.
"""

import argparse
import os
import sys
import requests
import xml.etree.ElementTree as ET
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC

# Base URL
BASE_URL = "https://analysiscenter.veracode.com/api/5.0"

# Optional: EU region support (auto-adjustable)
REGION_URLS = {
    "us": "https://analysiscenter.veracode.com/api/5.0",
    "eu": "https://analysiscenter.veracode.eu.com/api/5.0",
}


# -------------------- Utilities --------------------
def log(msg):
    print(msg, flush=True)


def get_app_id(app_name, region="us"):
    """Fetch app_id by app_name."""
    url = f"{REGION_URLS[region]}/getapplist.do"
    log(f"Resolving app_id for app_name='{app_name}' ...")

    response = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC())
    if response.status_code != 200:
        log(f"❌ Failed to retrieve app list. HTTP {response.status_code}")
        sys.exit(1)

    root = ET.fromstring(response.text)
    for app in root.findall(".//app"):
        if app.get("app_name") == app_name:
            return app.get("app_id")

    log(f"❌ App name '{app_name}' not found in your Veracode account.")
    sys.exit(1)


def get_latest_build_id(app_id, region="us"):
    """
    Get the latest build_id for the given app.
    - For DAST: look for dynamic_scan_type="ds"
    - For Static: return the most recent one
    """
    url = f"{REGION_URLS[region]}/getbuildlist.do?app_id={app_id}"
    log(f"Fetching build list for app_id={app_id} ...")

    response = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC())
    if response.status_code != 200:
        log(f"❌ Failed to retrieve build list. HTTP {response.status_code}")
        sys.exit(1)

    root = ET.fromstring(response.text)
    builds = root.findall(".//{https://analysiscenter.veracode.com/schema/2.0/buildlist}build")

    if not builds:
        log("⚠️  No builds found for this application.")
        sys.exit(1)

    # Try Dynamic first
    for build in reversed(builds):
        if build.get("dynamic_scan_type") == "ds" and build.get("policy_updated_date"):
            return build.get("build_id"), "Dynamic"

    # Fallback: Static (most recent build)
    latest_build = builds[-1]
    return latest_build.get("build_id"), "Static"


def get_build_info(app_id, build_id, scan_type, region="us"):
    """Fetch buildinfo for given build_id (DAST requires both app_id & build_id)."""
    url = f"{REGION_URLS[region]}/getbuildinfo.do?app_id={app_id}"
    if scan_type == "Dynamic":
        url += f"&build_id={build_id}"

    log(f"Fetching build info for app_id={app_id}, build_id={build_id} ({scan_type}) ...")

    response = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC())
    if response.status_code != 200:
        log(f"❌ Failed to retrieve build info. HTTP {response.status_code}")
        sys.exit(1)

    return response.text


def fetch_detailed_report(app_id, build_id, fmt, output_dir, prefix, region="us"):
    """Download the detailed report in XML or PDF."""
    if fmt.upper() == "PDF":
        endpoint = f"{REGION_URLS[region].replace('/5.0', '/4.0')}/detailedreportpdf.do"
        ext = "pdf"
    else:
        endpoint = f"{REGION_URLS[region]}/detailedreport.do"
        ext = "xml"

    url = f"{endpoint}?build_id={build_id}"
    log(f"Downloading detailed report ({fmt}) for build_id={build_id} ...")

    response = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC())
    if response.status_code != 200:
        log(f"❌ Failed to download report. HTTP {response.status_code}")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)
    filename = f"{prefix or ''}veracode_report_{build_id}.{ext}"
    file_path = os.path.join(output_dir, filename)

    with open(file_path, "wb") as f:
        f.write(response.content)

    log(f"✅ Report saved to: {file_path}")


# -------------------- Main Entry --------------------
def main():
    parser = argparse.ArgumentParser(description="Fetch Veracode Detailed Reports (Static/DAST).")
    parser.add_argument("-i", "--app_id", help="Veracode application ID")
    parser.add_argument("-n", "--app_name", help="Veracode application name")
    parser.add_argument("-f", "--format", required=True, choices=["XML", "PDF"], help="Report format")
    parser.add_argument("-o", "--output_dir", default=".", help="Output directory")
    parser.add_argument("-p", "--prefix", help="Filename prefix")
    parser.add_argument("-r", "--region", choices=["us", "eu"], default="us", help="Region selection (default: us)")

    args = parser.parse_args()

    if not args.app_id and not args.app_name:
        parser.error("You must specify either --app_id or --app_name.")

    # Resolve app_id if only app_name is given
    app_id = args.app_id or get_app_id(args.app_name, args.region)

    build_id, scan_type = get_latest_build_id(app_id, args.region)
    log(f"Detected scan type: {scan_type} | build_id={build_id}")

    # Fetch buildinfo (for logging/debug)
    _ = get_build_info(app_id, build_id, scan_type, args.region)

    # Download report
    fetch_detailed_report(app_id, build_id, args.format, args.output_dir, args.prefix, args.region)


if __name__ == "__main__":
    main()
