#!/usr/bin/env python3
"""
Example usage of the Veracode Detailed Report Fetcher module.

Demonstrates programmatic fetching of XML or PDF reports using HMAC authentication.
Supports app_id or app_name, region selection, output directory, and filename prefix.

Requires:
- Veracode HMAC credentials in ~/.veracode/credentials
- Installed package: veracode-detailed-report
"""

import os
from veracode_report.get_detailed_report import (
    get_build_id,
    fetch_detailed_report,
    resolve_app_id,
    REGIONS
)

def main():
    # -----------------------------
    # Configuration
    # -----------------------------
    app_id = None               # Use this if you want to fetch by ID
    app_name = "test_java"      # Use this if you want to fetch by name
    report_format = "PDF"       # Either "XML" or "PDF"
    region = "us"               # "us" or "eu"
    output_dir = "./reports"    # Directory to save reports
    prefix = "test_"            # Optional filename prefix

    api_base = REGIONS[region]

    # Resolve app_id if app_name is provided
    if not app_id and app_name:
        app_id = resolve_app_id(api_base, app_name)

    # Fetch latest build_id
    build_id = get_build_id(api_base, app_id)
    if not build_id:
        print("❌ No build found for this application.")
        return

    # Fetch and save report
    fetch_detailed_report(api_base, build_id, report_format, output_dir, prefix)

    # Print completion message
    report_path = os.path.join(output_dir, f"{prefix}detailed_report.{report_format.lower()}")
    print(f"\n✅ Done! Report saved at: {report_path}")


if __name__ == "__main__":
    app_id = "2223648"
    report_type = "XML"  # or "PDF"
    build_id = get_build_id(app_id)
    fetch_detailed_report(build_id, report_type)
