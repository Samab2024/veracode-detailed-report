import sys
import requests
import xml.etree.ElementTree as ET
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC

API_BASE = "https://analysiscenter.veracode.com"
HEADERS = {"User-Agent": "Veracode Detailed Report Fetcher"}

def get_build_id(app_id: str) -> str:
    """Fetch the latest build_id for an application ID."""
    try:
        response = requests.get(
            f"{API_BASE}/api/5.0/getbuildinfo.do?app_id={app_id}",
            auth=RequestsAuthPluginVeracodeHMAC(),
            headers=HEADERS,
        )
        response.raise_for_status()
    except requests.RequestException as e:
        print("❌ Failed to get build info:", e)
        sys.exit(1)

    try:
        root = ET.fromstring(response.text)
        ns = {"ns": root.tag.split('}')[0].strip('{')}
        build_elem = root.find(".//ns:build", ns)
        if build_elem is not None and "build_id" in build_elem.attrib:
            return build_elem.attrib["build_id"]
        else:
            print("⚠️  No build_id found in response XML.")
            sys.exit(1)
    except ET.ParseError as e:
        print("❌ Failed to parse XML response:", e)
        sys.exit(1)


def fetch_detailed_report(build_id: str, report_type: str) -> str:
    """Fetch and save Veracode detailed report (XML or PDF)."""
    report_type = report_type.upper()
    if report_type == "XML":
        endpoint = f"{API_BASE}/api/5.0/detailedreport.do?build_id={build_id}"
        filename = f"detailed_report_{build_id}.xml"
    elif report_type == "PDF":
        endpoint = f"{API_BASE}/api/4.0/detailedreportpdf.do?build_id={build_id}"
        filename = f"detailed_report_{build_id}.pdf"
    else:
        print("❌ Invalid report type. Use 'XML' or 'PDF'.")
        sys.exit(1)

    try:
        response = requests.get(endpoint, auth=RequestsAuthPluginVeracodeHMAC(), headers=HEADERS)
        response.raise_for_status()
    except requests.RequestException as e:
        print("❌ Failed to fetch detailed report:", e)
        sys.exit(1)

    # Save file (binary for PDF, text for XML)
    mode = "wb" if report_type == "PDF" else "w"
    with open(filename, mode) as f:
        if report_type == "PDF":
            f.write(response.content)
        else:
            f.write(response.text)

    print(f"✅ {report_type} report saved as {filename}")
    return filename


def main():
    if len(sys.argv) < 3:
        print("Usage: veracode-report <app_id> <report_type>")
        print("Example: veracode-report 2223648 XML")
        sys.exit(1)

    app_id = sys.argv[1]
    report_type = sys.argv[2]

    print(f"Fetching build info for app_id={app_id}...")
    build_id = get_build_id(app_id)
    print(f"Found build_id={build_id}, fetching {report_type} report...")
    fetch_detailed_report(build_id, report_type)


if __name__ == "__main__":
    main()
