#!/usr/bin/env python3
import argparse
import sys
import importlib

# Map task names to modules
TASK_MAP = {
    "detailed_report": detailed_report.run,
    "app_list": app_list.run,
    "app_info": app_info.run,
    "build_list": build_list.run,
    "build_info": build_info.run,
}

def main():
    parser = argparse.ArgumentParser(
        description="Unified CLI for Veracode XML API operations.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="task", help="Available tasks")
    
    # Add subparser for each task
    for task_name, module_path in TASK_MAP.items():
        module = importlib.import_module(module_path)
        # Each module exposes a setup_parser function to define its own arguments
        task_parser = subparsers.add_parser(task_name, help=module.HELP_TEXT)
        module.setup_parser(task_parser)

    args = parser.parse_args()

    if args.task is None:
        parser.print_help()
        sys.exit(1)

    # Import the task module and run
    task_module = importlib.import_module(TASK_MAP[args.task])
    task_module.run(args)


if __name__ == "__main__":
    sys.exit(main())
