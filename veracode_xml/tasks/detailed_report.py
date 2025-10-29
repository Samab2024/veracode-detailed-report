import os
from veracode_xml.utils.api_helpers import (
    get_app_id_from_name,
    get_latest_build_id,
    fetch_detailed_report,
)

HELP_TEXT = "Fetch detailed report (XML/PDF) for a specific app/build."

def setup_parser(parser):
    parser.add_argument("-i", "--app_id", help="Veracode App ID (required if --app_name not used)")
    parser.add_argument("-n", "--app_name", help="Veracode App Name (required if --app_id not used)")
    parser.add_argument("-f", "--format", choices=["XML", "PDF"], required=True, help="Report format")
    parser.add_argument("-s", "--scan_type", choices=["ss", "ds"], default="ss", help="Scan type (ss=Static, ds=Dynamic)")
    parser.add_argument("-r", "--region", choices=["us","eu","gov"], default="us", help="Region for API requests")
    parser.add_argument("-o", "--output_dir", default=".", help="Directory to save report")
    parser.add_argument("-p", "--prefix", help="Filename prefix")

def run(args):
    print("📘 Task: Fetch Detailed Report")

    # Determine app_id
    app_id = args.app_id
    if not app_id and args.app_name:
        print(f"Resolving app_id for app_name='{args.app_name}' ...")
        app_id = get_app_id_from_name(args.app_name)

    if not app_id:
        print("❌ Please provide a valid app_id or app_name.")
        return

    # Fetch build_id
    print(f"Fetching latest build for app_id={app_id} (scan_type={args.scan_type or 'ss'}) ...")
    build_id = get_latest_build_id(app_id, args.scan_type)

    if not build_id:
        print("❌ No valid build found for the specified scan type. Exiting.")
        return

    # Fetch report
    print(f"📄 Downloading {args.format} report for build_id={build_id} ...")
    os.makedirs(args.output_dir, exist_ok=True)
    fetch_detailed_report(app_id, build_id, args.format, args.output_dir, args.prefix)
    print("✅ Report downloaded successfully.")
