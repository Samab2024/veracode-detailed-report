#!/usr/bin/env python3
import argparse
import sys
import importlib

# List all supported tasks (matching modules under tasks/)
SUPPORTED_TASKS = [
    "detailed_report",
    "app_list",
    "app_info",
    "build_list",
    "build_info",
]

def main():
    parser = argparse.ArgumentParser(
        description="🧩 Veracode XML CLI — unified interface for Veracode XML API tasks",
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Create subcommands (e.g. veracode-xml detailed_report ...)
    subparsers = parser.add_subparsers(
        title="Available Tasks",
        dest="task",
        metavar="<task>"
    )

    # Dynamically load each task module and set up its parser
    for task_name in SUPPORTED_TASKS:
        try:
            module = importlib.import_module(f"veracode_xml.tasks.{task_name}")
            help_text = getattr(module, "HELP_TEXT", f"Execute the '{task_name}' task")
            task_parser = subparsers.add_parser(task_name, help=help_text)
            if hasattr(module, "setup_parser"):
                module.setup_parser(task_parser)
        except ModuleNotFoundError as e:
            print(f"⚠️  Warning: Task module '{task_name}' not found. ({e})")

    # Parse CLI arguments
    args = parser.parse_args()

    if args.task is None:
        parser.print_help()
        sys.exit(1)

    # Dynamically import the selected task module
    try:
        task_module = importlib.import_module(f"veracode_xml.tasks.{args.task}")
    except ModuleNotFoundError:
        print(f"❌ Task '{args.task}' is not implemented or missing.")
        sys.exit(1)

    # Run the selected task
    if hasattr(task_module, "run"):
        task_module.run(args)
    else:
        print(f"❌ Task '{args.task}' does not define a run(args) function.")
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
