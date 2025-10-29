from ..utils.api_helpers import get_veracode_session

def run(args):
    session = get_veracode_session(region=args.region)
    url = f"{session.api_base}/api/4.0/getapplist.do"
    
    response = session.get(url)
    if response.status_code != 200:
        print(f"❌ Failed to fetch app list: {response.status_code}")
        return
    
    # Parse XML
    root = response.xml_root()
    apps = root.findall(".//app", namespaces={"ns": root.nsmap.get(None)})
    if not apps:
        print("⚠️ No applications found.")
        return
    
    for app in apps:
        print(f"{app.attrib.get('app_id')} : {app.attrib.get('app_name')}")
