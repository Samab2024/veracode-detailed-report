"""
veracode_report package

Fetches Veracode Detailed Reports (XML/PDF) using HMAC authentication.
Supports Static and Dynamic (DAST) scans.
"""

from .get_detailed_report import (
    get_app_id,
    get_latest_build_id,
    get_build_info,
    fetch_detailed_report,
    main,
)

__all__ = [
    "get_app_id",
    "get_latest_build_id",
    "get_build_info",
    "fetch_detailed_report",
    "main",
]
