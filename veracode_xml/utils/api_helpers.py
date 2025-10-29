import requests
import xml.etree.ElementTree as ET
import os
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC

BASE_URL = "https://analysiscenter.veracode.com/api"

def get_app_id_from_name(app_name):
    """Get app_id using app_name."""
    try:
        url = f"{BASE_URL}/5.0/getapplist.do"
        response = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC())
        response.raise_for_status()
        root = ET.fromstring(response.text)

        for app in root.findall(".//app"):
            if app.get("app_name") == app_name:
                print(f"✅ Found app_id={app.get('app_id')}")
                return app.get("app_id")
        print(f"❌ App name '{app_name}' not found in your Veracode account.")
        return None
    except Exception as e:
        print(f"❌ Error fetching app list: {e}")
        return None


def get_latest_build_id(app_id, scan_type="ss"):
    """Fetch latest build_id depending on scan type."""
    try:
        if scan_type == "ds":
            url = f"{BASE_URL}/5.0/getbuildlist.do?app_id={app_id}"
            response = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC())
            response.raise_for_status()
            root = ET.fromstring(response.text)
            builds = root.findall(".//build")

            if not builds:
                print("❌ No dynamic scan builds found.")
                return None

            # Select the latest by policy_updated_date
            latest_build = max(builds, key=lambda b: b.get("policy_updated_date", ""))
            return latest_build.get("build_id")

        # Default to static scan
        url = f"{BASE_URL}/5.0/getbuildinfo.do?app_id={app_id}"
        response = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC())
        response.raise_for_status()
        root = ET.fromstring(response.text)
        build_elem = root.find(".//{https://analysiscenter.veracode.com/schema/4.0/buildinfo}build")

        if build_elem is not None:
            return build_elem.get("build_id")

        print("❌ No static scan builds found.")
        return None

    except Exception as e:
        print(f"❌ Error fetching build list: {e}")
        return None


def fetch_detailed_report(app_id, build_id, format_type, output_dir, prefix):
    """Download detailed report as XML or PDF."""
    try:
        if format_type == "PDF":
            url = f"{BASE_URL}/4.0/detailedreportpdf.do?build_id={build_id}&app_id={app_id}"
            extension = "pdf"
        else:
            url = f"{BASE_URL}/5.0/detailedreport.do?build_id={build_id}&app_id={app_id}"
            extension = "xml"

        response = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC())
        response.raise_for_status()

        filename = f"{prefix}{app_id}_{build_id}.{extension}"
        file_path = os.path.join(output_dir, filename)

        with open(file_path, "wb") as f:
            f.write(response.content)

        print(f"✅ Report saved to {file_path}")
        return file_path

    except Exception as e:
        print(f"❌ Failed to fetch detailed report: {e}")
        return None
