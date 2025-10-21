"""
veracode_report package initialization.
Exposes core functions for fetching Veracode detailed reports.
"""

from .get_detailed_report import (
    get_app_id_from_name,
    get_latest_build_id,
    fetch_detailed_report,
    main,
)

__all__ = [
    "get_app_id_from_name",
    "get_latest_build_id",
    "fetch_detailed_report",
    "main",
]
