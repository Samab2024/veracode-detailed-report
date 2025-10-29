from ..utils.api_helpers import get_veracode_session, resolve_app_id

HELP_TEXT = "Fetch detailed information for a specific application."

def setup_parser(parser):
    parser.add_argument("-i", "--app_id", help="Veracode App ID (required if --app_name not used)")
    parser.add_argument("-n", "--app_name", help="Veracode App Name (required if --app_id not used)")
    parser.add_argument("-r", "--region", choices=["us","eu","gov"], default="us", help="Region for API requests")

def run(args):
    session = get_veracode_session(region=args.region)
    app_id = args.app_id or resolve_app_id(args.app_name, session)
    
    if not app_id:
        print(f"❌ App not found.")
        return
    
    url = f"{session.api_base}/api/4.0/getappinfo.do?app_id={app_id}"
    response = session.get(url)
    
    if response.status_code != 200:
        print(f"❌ Failed to fetch app info: {response.status_code}")
        return
    
    root = response.xml_root()
    print(f"App Name: {root.attrib.get('app_name')}")
    print(f"App ID: {root.attrib.get('app_id')}")
    print(f"Description: {root.attrib.get('description')}")
