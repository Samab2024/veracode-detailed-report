"""
Veracode Detailed Report Fetcher Package
========================================

A lightweight Python module to fetch Veracode Detailed Reports (XML or PDF)
using HMAC authentication.

Functions
---------
- get_build_id(app_id): Fetches the latest build ID for a given application.
- fetch_detailed_report(build_id, report_type): Downloads the detailed report in XML or PDF format.

CLI
---
This package also exposes a command-line tool:
    veracode-report <app_id> <report_type>

Example
-------
>>> from veracode_report import get_build_id, fetch_detailed_report
>>> build_id = get_build_id("2223648")
>>> fetch_detailed_report(build_id, "XML")
"""

from .get_detailed_report import get_build_id, fetch_detailed_report

__all__ = ["get_build_id", "fetch_detailed_report"]

__version__ = "1.0.0"
__author__ = "Your Name"
__license__ = "MIT" 
