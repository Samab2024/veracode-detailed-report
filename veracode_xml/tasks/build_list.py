from ..utils.api_helpers import get_veracode_session, resolve_app_id

HELP_TEXT = "List all builds for a specific application."

def setup_parser(parser):
    parser.add_argument("-i", "--app_id", help="Veracode App ID (required if --app_name not used)")
    parser.add_argument("-n", "--app_name", help="Veracode App Name (required if --app_id not used)")
    parser.add_argument("-s", "--scan_type", choices=["ss","ds"], default="ss", help="Filter by scan type")
    parser.add_argument("-r", "--region", choices=["us","eu","gov"], default="us", help="Region for API requests")

def run(args):
    session = get_veracode_session(region=args.region)
    app_id = args.app_id or resolve_app_id(args.app_name, session)
    
    if not app_id:
        print(f"❌ App not found.")
        return
    
    url = f"{session.api_base}/api/2.0/getbuildlist.do?app_id={app_id}"
    response = session.get(url)
    
    if response.status_code != 200:
        print(f"❌ Failed to fetch build list: {response.status_code}")
        return
    
    root = response.xml_root()
    builds = root.findall(".//build", namespaces={"ns": root.nsmap.get(None)})
    
    if not builds:
        print(f"⚠️ No builds found for app_id={app_id}")
        return
    
    for build in builds:
        if args.scan_type and build.attrib.get("dynamic_scan_type") != args.scan_type:
            continue
        print(f"{build.attrib.get('build_id')} : {build.attrib.get('version')} ({build.attrib.get('dynamic_scan_type')})")
