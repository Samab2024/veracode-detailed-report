from veracode_report.get_detailed_report import get_build_id, fetch_detailed_report

if __name__ == "__main__":
    app_id = "2223648"
    report_type = "XML"  # or "PDF"
    build_id = get_build_id(app_id)
    fetch_detailed_report(build_id, report_type)
