#!/usr/bin/env python3
"""
veracode_report/get_detailed_report.py

Generates a detailed Veracode report for an application.
Supports both Static (ss) and Dynamic (ds) scans.
"""

import argparse
import os
import sys
import requests
import xml.etree.ElementTree as ET
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC


# ==============================================================
# Utility: Get App ID from App Name
# ==============================================================

def get_app_id_from_name(app_name):
    """Fetch app_id for the given app_name, handles XML namespace"""
    url = "https://analysiscenter.veracode.com/api/5.0/getapplist.do"
    resp = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC())
    resp.raise_for_status()

    root = ET.fromstring(resp.text)

    # detect namespace
    ns = {"ns": root.tag.split("}")[0].strip("{")} if "}" in root.tag else {}

    # search using namespace
    for app in root.findall(".//ns:app", ns):
        if app.get("app_name") == app_name:
            print(f"✅ Found app_id={app.get('app_id')}")
            return app.get("app_id")

    print(f"❌ App name '{app_name}' not found in your Veracode account.")
    return None


# ==============================================================
# Utility: Get Latest Build ID (Static or Dynamic)
# ==============================================================

def get_latest_build_id(app_id, scan_type="ss"):
    import requests
    import xml.etree.ElementTree as ET
    from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC

    base_url = "https://analysiscenter.veracode.com/api/5.0"
    headers = {"User-Agent": "veracode-report/2.0"}

    if scan_type == "ss":
        url = f"{base_url}/getbuildinfo.do?app_id={app_id}"
        r = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC(), headers=headers)
        r.raise_for_status()
        root = ET.fromstring(r.text)

        # Detect namespace dynamically
        if "}" in root.tag:
            ns = {"ns": root.tag.split("}")[0].strip("{")}
            build_elem = root.find(".//ns:build", ns)
        else:
            build_elem = root.find(".//build")

        if build_elem is not None:
            return build_elem.get("build_id")

        print(f"⚠️ No {scan_type.upper()} builds found for app_id={app_id}.")
        return None

    elif scan_type == "ds":
        url = f"{base_url}/getbuildlist.do?app_id={app_id}"
        r = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC(), headers=headers)
        r.raise_for_status()
        root = ET.fromstring(r.text)

        # Detect namespace dynamically
        if "}" in root.tag:
            ns = {"ns": root.tag.split("}")[0].strip("{")}
            builds = root.findall(".//ns:build", ns)
        else:
            builds = root.findall(".//build")

        ds_builds = [b for b in builds if b.get("dynamic_scan_type") == "ds"]
        if not ds_builds:
            print(f"⚠️ No dynamic scan builds found for app_id={app_id}.")
            return None

        latest_build = sorted(
            ds_builds, key=lambda b: b.get("policy_updated_date") or "", reverse=True
        )[0]

        return latest_build.get("build_id")

    else:
        print(f"⚠️ Unknown scan_type={scan_type}")
        return None


# ==============================================================
# Fetch Detailed Report (XML, PDF, or CSV)
# ==============================================================

def fetch_detailed_report(app_id, build_id, report_format, output_dir, prefix):
    """Download detailed report for given build_id and app_id"""
    base_url = "https://analysiscenter.veracode.com/api/5.0"
    format_ext = report_format.lower()
    url = f"{base_url}/detailedreport.do?app_id={app_id}&build_id={build_id}"

    if format_ext in ["pdf", "xml", "csv"]:
        url += f"&report_format={format_ext}"
    else:
        print(f"⚠️ Unsupported report format '{report_format}'. Defaulting to XML.")
        format_ext = "xml"
        url += "&report_format=xml"

    print(f"📥 Fetching {report_format.upper()} report for build_id={build_id} ...")

    response = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC())
    response.raise_for_status()

    filename = f"{prefix}{app_id}_build_{build_id}_report.{format_ext}"
    output_path = os.path.join(os.path.expanduser(output_dir), filename)

    with open(output_path, "wb") as f:
        f.write(response.content)

    print(f"✅ Report saved to: {output_path}")


# ==============================================================
# Main Entry Point
# ==============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Generate Veracode Detailed Report (Static or Dynamic)"
    )

    parser.add_argument("-a", "--app_id", help="Veracode application ID")
    parser.add_argument("-n", "--app_name", help="Veracode application name")
    parser.add_argument("-f", "--format", required=True, help="Report format: PDF | XML | CSV")
    parser.add_argument("-s", "--scan_type", default="ss", help="Scan type: ss (Static) | ds (Dynamic)")
    parser.add_argument("-o", "--output_dir", default=".", help="Output directory for report")
    parser.add_argument("-p", "--prefix", default="", help="Filename prefix")

    args = parser.parse_args()

    # Determine app_id
    app_id = args.app_id
    if not app_id and args.app_name:
        print(f"Resolving app_id for app_name='{args.app_name}' ...")
        app_id = get_app_id_from_name(args.app_name)
    if not app_id:
        print("❌ Please provide a valid app_id or app_name.")
        sys.exit(1)

    # Determine latest build_id based on scan type
    print(f"Fetching latest build for app_id={app_id} (scan_type={args.scan_type}) ...")
    build_id = get_latest_build_id(app_id, scan_type=args.scan_type)
    if not build_id:
        print("❌ No build found. Exiting.")
        sys.exit(1)

    # Fetch report
    fetch_detailed_report(app_id, build_id, args.format, args.output_dir, args.prefix)


if __name__ == "__main__":
    main()
