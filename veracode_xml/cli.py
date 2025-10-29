#!/usr/bin/env python3
import argparse
import sys
import importlib

# Map task names to their module paths
TASK_MAP = {
    "detailed_report": "veracode_xml.tasks.detailed_report",
    "app_list": "veracode_xml.tasks.app_list",
    "app_info": "veracode_xml.tasks.app_info",
    "build_list": "veracode_xml.tasks.build_list",
    "build_info": "veracode_xml.tasks.build_info",
}

def main():
    parser = argparse.ArgumentParser(
        description="Unified CLI for Veracode XML API operations.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Top-level subparsers for tasks
    subparsers = parser.add_subparsers(dest="task", title="Available tasks", metavar="{task}", help="Choose one task to run")

    # Add subparser for each task dynamically
    for task_name, module_path in TASK_MAP.items():
        module = importlib.import_module(module_path)
        task_parser = subparsers.add_parser(
            task_name,
            help=getattr(module, "HELP_TEXT", ""),
            description=getattr(module, "HELP_TEXT", "")
        )
        # Each task defines its own setup_parser() to add arguments
        module.setup_parser(task_parser)

    # Parse args
    args = parser.parse_args()

    # If no task provided, show top-level help
    if args.task is None:
        parser.print_help()
        sys.exit(1)

    # Dynamically import and run the selected task
    task_module = importlib.import_module(TASK_MAP[args.task])
    task_module.run(args)


if __name__ == "__main__":
    sys.exit(main())
