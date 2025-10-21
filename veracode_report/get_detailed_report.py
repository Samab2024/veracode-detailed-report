import os
import sys
import argparse
import requests
import xml.etree.ElementTree as ET
from pathlib import Path
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC

# Default regions
REGION_ENDPOINTS = {
    "us": "https://analysiscenter.veracode.com",
    "eu": "https://analysiscenter.veracode.eu"
}

def get_app_id_by_name(api_base, app_name):
    """Fetch app_id from app_name using getapplist API."""
    try:
        response = requests.get(
            f"{api_base}/api/5.0/getapplist.do",
            auth=RequestsAuthPluginVeracodeHMAC(),
            headers={"User-Agent": "Python HMAC Example"}
        )
        response.raise_for_status()
        root = ET.fromstring(response.text)
        for app in root.findall(".//app"):
            if app.attrib.get("app_name") == app_name:
                return app.attrib.get("app_id")
        print(f"❌ No application found with name '{app_name}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error fetching app_id for {app_name}: {e}")
        sys.exit(1)

def get_build_id(api_base, app_id, sandbox_id=None):
    """Fetch the latest build_id for a given app_id (and optional sandbox)."""
    url = f"{api_base}/api/5.0/getbuildinfo.do?app_id={app_id}"
    if sandbox_id:
        url += f"&sandbox_id={sandbox_id}"

    print(f"Fetching build info for app_id={app_id} ...")
    try:
        response = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC())
        response.raise_for_status()
        root = ET.fromstring(response.text)
        build_id = root.attrib.get("build_id")
        if not build_id:
            print("⚠️  No build_id found in response XML.")
            print(response.text)
            sys.exit(1)
        print(f"✅ Found build_id: {build_id}")
        return build_id
    except Exception as e:
        print(f"Error fetching build info: {e}")
        sys.exit(1)

def fetch_detailed_report(api_base, build_id, report_type, output_dir, prefix):
    """Download XML or PDF detailed report and save to output directory."""
    if report_type.upper() == "XML":
        endpoint = f"{api_base}/api/5.0/detailedreport.do?build_id={build_id}"
        ext = "xml"
    elif report_type.upper() == "PDF":
        endpoint = f"{api_base}/api/4.0/detailedreportpdf.do?build_id={build_id}"
        ext = "pdf"
    else:
        print("❌ Invalid report type. Use XML or PDF.")
        sys.exit(1)

    try:
        response = requests.get(endpoint, auth=RequestsAuthPluginVeracodeHMAC())
        response.raise_for_status()

        Path(output_dir).mkdir(parents=True, exist_ok=True)
        output_path = os.path.join(output_dir, f"{prefix}{build_id}.{ext}")

        with open(output_path, "wb") as f:
            f.write(response.content)

        print(f"✅ Report saved at: {output_path}")
        return output_path
    except Exception as e:
        print(f"Error fetching detailed report: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Fetch Veracode Detailed Report (XML/PDF)")
    parser.add_argument("--app_id", help="Veracode application ID")
    parser.add_argument("--app_name", help="Veracode application name (alternative to app_id)")
    parser.add_argument("--sandbox_id", help="Optional sandbox ID")
    parser.add_argument("--region", choices=["us", "eu"], default="us", help="Veracode region (default: us)")
    parser.add_argument("--output_dir", default="reports", help="Directory to save reports")
    parser.add_argument("--prefix", default="veracode_", help="Filename prefix for output files")
    parser.add_argument("--report_type", choices=["XML", "PDF"], required=True, help="Type of report to download")

    args = parser.parse_args()

    api_base = REGION_ENDPOINTS[args.region]
    print(f"🌍 Using region endpoint: {api_base}")

    # Resolve app_id if only app_name is provided
    if not args.app_id and args.app_name:
        args.app_id = get_app_id_by_name(api_base, args.app_name)
    elif not args.app_id:
        print("❌ You must provide either --app_id or --app_name")
        sys.exit(1)

    build_id = get_build_id(api_base, args.app_id, args.sandbox_id)
    fetch_detailed_report(api_base, build_id, args.report_type, args.output_dir, args.prefix)

if __name__ == "__main__":
    main()
