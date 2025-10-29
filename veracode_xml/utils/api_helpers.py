import os
import requests
import xml.etree.ElementTree as ET
from veracode_xml.config import (
    endpoint_getapplist,
    endpoint_getbuildlist,
    endpoint_getbuildinfo,
    endpoint_detailedreport_xml,
    endpoint_detailedreport_pdf,
    DEFAULT_REGION,
)
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC

def _parse_xml_with_ns(text):
    """
    Parse XML text and return tuple (root, ns_map)
    where ns_map is a dict like {'ns': <namespace_uri>} if namespace exists.
    """
    root = ET.fromstring(text)
    ns_map = {}
    if "}" in root.tag:
        uri = root.tag.split("}")[0].strip("{")
        ns_map = {"ns": uri}
    return root, ns_map

def get_app_id_from_name(app_name: str, region: str = DEFAULT_REGION) -> str | None:
    """Look up app_id for a given application name, handling namespace correctly."""
    url = endpoint_getapplist(region)
    resp = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC())
    resp.raise_for_status()

    root, ns = _parse_xml_with_ns(resp.text)
    # pick the correct tag path
    if ns:
        apps = root.findall(".//ns:app", ns)
    else:
        apps = root.findall(".//app")

    for app in apps:
        if app.get("app_name") == app_name:
            return app.get("app_id")

    return None

def get_latest_build_id(app_id: str, scan_type: str = "ss", region: str = DEFAULT_REGION) -> str | None:
    """
    Fetch latest build_id depending on scan type.
    scan_type: "ss" (Static) or "ds" (Dynamic)
    """
    if scan_type == "ds":
        url = endpoint_getbuildlist(region) + f"?app_id={app_id}"
        resp = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC())
        resp.raise_for_status()
        root, ns = _parse_xml_with_ns(resp.text)
        if ns:
            builds = root.findall(".//ns:build", ns)
        else:
            builds = root.findall(".//build")

        ds_builds = [b for b in builds if b.get("dynamic_scan_type") == "ds" and b.get("policy_updated_date")]
        if not ds_builds:
            return None

        latest = max(ds_builds, key=lambda b: b.get("policy_updated_date", ""))
        return latest.get("build_id")

    else:
        url = endpoint_getbuildinfo(region) + f"?app_id={app_id}"
        resp = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC())
        resp.raise_for_status()
        root, ns = _parse_xml_with_ns(resp.text)

        if ns:
            build_elem = root.find(".//ns:build", ns)
        else:
            build_elem = root.find(".//build")

        if build_elem is not None:
            return build_elem.get("build_id")

        return None

def fetch_detailed_report(app_id: str, build_id: str, format_type: str, output_dir: str, prefix: str, region: str = DEFAULT_REGION) -> str | None:
    """Download detailed report (XML or PDF) and save locally."""
    format_type = format_type.upper()
    if format_type == "PDF":
        url = endpoint_detailedreport_pdf(region) + f"?build_id={build_id}&app_id={app_id}"
        extension = "pdf"
    else:
        url = endpoint_detailedreport_xml(region) + f"?build_id={build_id}&app_id={app_id}"
        extension = "xml"

    resp = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC())
    resp.raise_for_status()

    os.makedirs(os.path.expanduser(output_dir), exist_ok=True)
    filename = f"{prefix}{app_id}_{build_id}_report.{extension}"
    filepath = os.path.join(os.path.expanduser(output_dir), filename)

    with open(filepath, "wb") as f:
        f.write(resp.content)

    return filepath
