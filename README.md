# Veracode Detailed Report Fetcher

A Python utility to fetch **Veracode Detailed Reports (XML or PDF)** using HMAC authentication.

Built with [veracode-api-signing](https://github.com/veracode/veracode-python-hmac-example).

---

## 🚀 Features
- Uses Veracode HMAC authentication.
- Fetches the latest `build_id` automatically.
- Downloads XML or PDF detailed reports.
- CLI and importable module.

---

## 🧩 Installation
```
bash
git clone https://github.com/<your-username>/veracode-detailed-report.git
cd veracode-detailed-report
pip install -r requirements.txt
pip install .
```
---

## ⚙️ Usage
```
Command-line:

veracode-report <app_id> <report_type>

Examples:

veracode-report 2223648 XML
veracode-report 2223648 PDF


Programmatic (Python):

from veracode_report.get_detailed_report import get_build_id, fetch_detailed_report

build_id = get_build_id("2223648")
fetch_detailed_report(build_id, "PDF")
```
---

## 🪪 Authentication
```
Requires Veracode HMAC credentials:

~/.veracode/credentials

with:

[default]
veracode_api_key_id = YOUR_KEY_ID
veracode_api_key_secret = YOUR_KEY_SECRET
```
---

## 📜 License

MIT License
