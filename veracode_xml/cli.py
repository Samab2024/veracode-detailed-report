#!/usr/bin/env python3
import argparse
import sys
from veracode_xml.tasks import detailed_report

# Task registry
TASKS = {
    "detailed_report": detailed_report.run,
}

def main():
    parser = argparse.ArgumentParser(
        prog="veracode-xml",
        description="Unified CLI for Veracode XML API operations."
    )

    parser.add_argument(
        "-t", "--task",
        required=True,
        choices=TASKS.keys(),
        help="Specify task to run (e.g., detailed_report)"
    )
    parser.add_argument("-a", "--app_id", help="Veracode Application ID")
    parser.add_argument("-n", "--app_name", help="Veracode Application Name")
    parser.add_argument("-f", "--format", choices=["XML", "PDF"], required=True, help="Report format")
    parser.add_argument("-s", "--scan_type", choices=["ss", "ds"], help="Scan type: ss (Static), ds (Dynamic)")
    parser.add_argument("-o", "--output_dir", default=".", help="Output directory for reports")
    parser.add_argument("-p", "--prefix", default="", help="Filename prefix")

    args = parser.parse_args()

    try:
        TASKS[args.task](args)
    except Exception as e:
        print(f"❌ Error executing task '{args.task}': {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
