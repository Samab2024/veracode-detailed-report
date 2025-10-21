import sys
import os
import argparse
import requests
import xml.etree.ElementTree as ET
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC

# Supported regions
REGIONS = {
    "us": "https://analysiscenter.veracode.com",
    "eu": "https://analysiscenter.veracode.eu",
}

headers = {"User-Agent": "Veracode Detailed Report Fetcher"}


def resolve_app_id(api_base, app_name):
    """Resolve app_id given an app_name."""
    print(f"Resolving app_id for app_name='{app_name}' ...")
    try:
        resp = requests.get(
            f"{api_base}/api/5.0/getapplist.do",
            auth=RequestsAuthPluginVeracodeHMAC(),
            headers=headers,
        )
        resp.raise_for_status()
        root = ET.fromstring(resp.text)

        for app in root.findall(".//app"):
            if app.get("app_name") == app_name:
                app_id = app.get("app_id")
                print(f"✅ Found app_id={app_id} for app_name={app_name}")
                return app_id

        print(f"❌ App name '{app_name}' not found in your Veracode account.")
        sys.exit(1)

    except requests.RequestException as e:
        print("Error fetching application list:")
        print(e)
        sys.exit(1)


def get_build_id(api_base, app_id):
    """Fetch the latest build_id for a given app_id."""
    print(f"Fetching build info for app_id={app_id} ...")
    try:
        response = requests.get(
            f"{api_base}/api/5.0/getbuildinfo.do?app_id={app_id}",
            auth=RequestsAuthPluginVeracodeHMAC(),
            headers=headers,
        )
        response.raise_for_status()

        root = ET.fromstring(response.text)
        build = root.find(".//build")
        if build is not None and "build_id" in build.attrib:
            build_id = build.attrib["build_id"]
            print(f"✅ Found build_id={build_id}")
            return build_id
        else:
            print("⚠️ No build_id found in response XML.")
            return None

    except requests.RequestException as e:
        print("Error fetching build info:")
        print(e)
        sys.exit(1)


def fetch_detailed_report(api_base, build_id, report_format, output_dir, prefix):
    """Fetch detailed report (XML or PDF)."""
    report_format = report_format.upper()
    if report_format == "PDF":
        endpoint = "/api/4.0/detailedreportpdf.do"
        ext = "pdf"
    else:
        endpoint = "/api/5.0/detailedreport.do"
        ext = "xml"

    output_dir = os.path.expanduser(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"{prefix or ''}detailed_report.{ext}")

    print(f"Downloading {report_format} report to {filename} ...")

    try:
        response = requests.get(
            f"{api_base}{endpoint}?build_id={build_id}",
            auth=RequestsAuthPluginVeracodeHMAC(),
            headers=headers,
        )
        response.raise_for_status()

        with open(filename, "wb") as f:
            f.write(response.content)

        print(f"✅ Report saved: {filename}")

    except requests.RequestException as e:
        print("Error fetching detailed report:")
        print(e)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch Veracode detailed report (XML or PDF) using app_id or app_name."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--app_id", help="Veracode application ID")
    group.add_argument("--app_name", help="Veracode application name")
    parser.add_argument("--format", required=True, choices=["XML", "PDF"], help="Report format to download")
    parser.add_argument("--region", choices=["us", "eu"], default="us", help="Veracode region (default: us)")
    parser.add_argument("--output_dir", default=".", help="Output directory for reports")
    parser.add_argument("--prefix", default="", help="Optional prefix for output filename")

    args = parser.parse_args()
    api_base = REGIONS[args.region]

    # Resolve app_id
    app_id = args.app_id
    if not app_id and args.app_name:
        app_id = resolve_app_id(api_base, args.app_name)

    # Fetch build and report
    build_id = get_build_id(api_base, app_id)
    if not build_id:
        print("❌ No build found for this application.")
        sys.exit(1)

    fetch_detailed_report(api_base, build_id, args.format, args.output_dir, args.prefix)


if __name__ == "__main__":
    main()
