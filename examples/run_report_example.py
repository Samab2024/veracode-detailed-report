#!/usr/bin/env python3
"""
Example usage of the Veracode Detailed Report Fetcher module.

This script demonstrates how to programmatically fetch XML or PDF
Veracode detailed reports using HMAC authentication.

Requires:
- Veracode API credentials configured in ~/.veracode/credentials
- Installed package: veracode-detailed-report
"""

import os
from veracode_report.get_detailed_report import (
    get_api_base,
    get_app_id_from_name,
    get_build_id,
    fetch_detailed_report,
)

def main():
    # -------------------------------------------------------------------------
    # Configuration
    # -------------------------------------------------------------------------
    region = "us"  # Change to "eu" for European region
    report_type = "XML"  # or "PDF"
    app_identifier = "2223648"  # Can be app_id (numeric) or app_name (string)
    output_dir = "./reports"
    prefix = "veracode_"

    # -------------------------------------------------------------------------
    # Determine base URL and resolve app_id if needed
    # -------------------------------------------------------------------------
    api_base = get_api_base(region)

    if app_identifier.isdigit():
        app_id = app_identifier
        print(f"Using app_id: {app_id}")
    else:
        app_id = get_app_id_from_name(api_base, app_identifier)

    # -------------------------------------------------------------------------
    # Fetch build_id for the app
    # -------------------------------------------------------------------------
    build_id = get_build_id(api_base, app_id)

    # -------------------------------------------------------------------------
    # Fetch and save the detailed report
    # -------------------------------------------------------------------------
    fetch_detailed_report(api_base, build_id, report_type, output_dir, prefix)

    # -------------------------------------------------------------------------
    # Completion message
    # -------------------------------------------------------------------------
    report_path = os.path.join(output_dir, f"{prefix}{build_id}.{report_type.lower()}")
    print(f"\n✅ Done! Report saved at: {report_path}")


if __name__ == "__main__":
    main()
