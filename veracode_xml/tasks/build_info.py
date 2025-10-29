from ..utils.api_helpers import get_veracode_session, resolve_app_id, get_latest_build_id

HELP_TEXT = "Fetch build info for a specific build or latest build."

def setup_parser(parser):
    parser.add_argument("-i", "--app_id", help="Veracode App ID (required if --app_name not used)")
    parser.add_argument("-n", "--app_name", help="Veracode App Name (required if --app_id not used)")
    parser.add_argument("-b", "--build_id", help="Specific build ID (optional; fetch latest if omitted)")
    parser.add_argument("-s", "--scan_type", choices=["ss","ds"], default="ss", help="Scan type (ss=Static, ds=Dynamic)")
    parser.add_argument("-r", "--region", choices=["us","eu","gov"], default="us", help="Region for API requests")

def run(args):
    """
    Fetches build info for a given build_id or the latest build for the app.
    
    Required:
        --app_id OR --app_name
    Optional:
        --build_id (if not provided, fetch latest)
        --scan_type (default: ss)
        --region (default: us)
    """
    session = get_veracode_session(region=args.region)

    if not args.app_id and not args.app_name:
        print("❌ Please provide --app_id or --app_name")
        return

    app_id = args.app_id or resolve_app_id(args.app_name, session)
    if not app_id:
        print(f"❌ App '{args.app_name}' not found in your Veracode account.")
        return

    # Determine which build_id to use
    build_id = args.build_id
    if not build_id:
        # Fetch latest build based on scan_type
        build_id = get_latest_build_id(app_id, scan_type=args.scan_type, session=session)
        if not build_id:
            print(f"❌ No {args.scan_type.upper()} builds found for app_id={app_id}")
            return
        print(f"✅ Latest build_id={build_id} selected for app_id={app_id}")

    url = f"{session.api_base}/api/4.0/getbuildinfo.do?app_id={app_id}&build_id={build_id}"
    response = session.get(url)

    if response.status_code != 200:
        print(f"❌ Failed to fetch build info: {response.status_code}")
        return

    # Parse XML and namespace
    root = response.xml_root()
    ns = {"ns": root.nsmap.get(None)}
    build = root.find(".//ns:build", namespaces=ns)
    if not build:
        print(f"⚠️ No build info found for build_id={build_id}")
        return

    print(f"Build ID: {build.attrib.get('build_id')}")
    print(f"Version: {build.attrib.get('version')}")
    print(f"Scan Type: {build.attrib.get('dynamic_scan_type') or 'ss'}")
    print(f"Results Ready: {build.attrib.get('results_ready')}")
    print(f"Policy Compliance: {build.attrib.get('policy_compliance_status')}")
    print(f"Policy Updated Date: {build.attrib.get('policy_updated_date')}")
