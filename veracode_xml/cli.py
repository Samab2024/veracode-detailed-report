#!/usr/bin/env python3
import argparse
import sys
import importlib

# Map task names to modules
TASK_MAP = {
    "detailed_report": "tasks.detailed_report",
    "app_list": "tasks.app_list",
    "app_info": "tasks.app_info",
    "build_list": "tasks.build_list",
    "build_info": "tasks.build_info",
}

def main():
    parser = argparse.ArgumentParser(
        description="Unified CLI for Veracode XML API operations.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "-t", "--task",
        choices=list(TASK_MAP.keys()),
        required=True,
        help="Specify task to run. Supported tasks:\n" +
             "\n".join([f"  {k}" for k in TASK_MAP.keys()])
    )

    # Only parse known args here; each task will handle its own parameters
    args, unknown = parser.parse_known_args()

    # Import task dynamically
    task_module = importlib.import_module(TASK_MAP[args.task])

    # Invoke the task's run() function, passing all args including unknown
    # Each task should have its own ArgumentParser for task-specific args
    task_module.run(sys.argv[1:])  # pass full CLI args for task parser

if __name__ == "__main__":
    sys.exit(main())
