"""
Fetch information for a specific application.
Reference: https://docs.veracode.com/r/r_getappinfo
"""

import argparse
import sys
import requests
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC
from veracode_xml.utils.file_utils import save_output, pretty_print_xml
from veracode_xml.helpers import get_api_base, find_app_by_name


def add_subparser(subparsers):
    parser = subparsers.add_parser(
        "app_info",
        help="Fetch detailed information about a Veracode application",
    )
    parser.add_argument("-a", "--app_id", help="Veracode application ID")
    parser.add_argument("-n", "--app_name", help="Veracode application name (alternate to --app_id)")
    parser.add_argument("-r", "--region", help="Veracode region (us, eu, us_fed)")
    parser.set_defaults(func=run)


def run(args):
    try:
        # Resolve app_id from app_name if needed
        if not args.app_id and args.app_name:
            print(f"🔍 Searching for application matching name: '{args.app_name}' ...")
            app_id = find_app_id_by_name(args.app_name, args.region)
            if not app_id:
                print("❌ No matching applications found.")
                sys.exit(1)
            args.app_id = app_id

        if not args.app_id:
            print("❌ Either --app_id or --app_name must be provided.")
            sys.exit(1)

        print(f"📡 Fetching app info for app_id={args.app_id} ...")

        api_base = get_api_base(args.region)
        url = f"{api_base}/api/5.0/getappinfo.do?app_id={args.app_id}"
        response = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC())

        if response.status_code != 200:
            print(f"❌ API request failed with status {response.status_code}: {response.text}")
            sys.exit(1)

        content = response.text
        if "<application" not in content:
            print("⚠️  No app info found.")
        else:
            pretty_print_xml(content)

        # Save result
        save_output(content, args, "app_info")

    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def find_app_id_by_name(app_name, region=None):
    """
    Find an app_id given a full or partial app name.
    Prompts the user if multiple matches are found.
    """
    apps = find_app_by_name(app_name, region)
    if not apps:
        return None

    if len(apps) == 1:
        app = apps[0]
        print(f"✅ Found application: {app['app_name']} (ID: {app['app_id']})")
        return app["app_id"]

    # Multiple matches
    print("\n⚠️  Multiple matches found:")
    for i, app in enumerate(apps, 1):
        print(f"  [{i}] {app['app_name']} (ID: {app['app_id']})")

    while True:
        choice = input("Enter the number of the application you want to use: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(apps):
            selected = apps[int(choice) - 1]
            print(f"✅ Selected: {selected['app_name']} (ID: {selected['app_id']})")
            return selected["app_id"]
        print("Invalid choice. Please try again.")
