# Veracode Detailed Report Fetcher

A Python utility to fetch **Veracode Detailed Reports (XML or PDF)** using HMAC authentication.

Built with [veracode-api-signing](https://github.com/veracode/veracode-python-hmac-example).

---

## 🚀 Features
- 🔐 Uses Veracode HMAC authentication.
- 🌍 Supports **US** and **EU** Veracode regions.
- 🧩 Fetches the latest `build_id` automatically.
- 🧠 Accepts either `app_id` or `app_name`.
- 💾 Allows custom output directory and filename prefix.
- 💻 Works as both a CLI tool and Python module.

---

## 🧩 Installation
```
bash
git clone https://github.com/Samab2024/veracode-detailed-report.git
cd veracode-detailed-report
pip install -r requirements.txt
pip install .
```
---

## ⚙️ Usage
```
Command-line:
Once installed, you can run the CLI command:
veracode-report <app_id_or_name> <report_type> [OPTIONS]

Arguments
Argument	Description	Example
<app_id_or_name>	Veracode Application ID or Name	2223648 / "MyApp"
<report_type>	Type of report to fetch (XML or PDF)	XML
Optional Flags
Option	Description	Example
--region	Veracode region (us or eu, default: us)	--region eu
--output_dir	Directory to save reports (default: ./reports)	--output_dir ./out
--prefix	Filename prefix (default: veracode_)	--prefix build_
Examples
Fetch an XML report by app ID (US region)
veracode-report 2223648 XML

Fetch a PDF report by app name (EU region)
veracode-report "MyApp" PDF --region eu --output_dir ./out --prefix build_

Programmatic (Python)
from veracode_report.get_detailed_report import get_build_id, fetch_detailed_report

api_base = "https://analysiscenter.veracode.com"
app_id = "2223648"
build_id = get_build_id(api_base, app_id)
fetch_detailed_report(api_base, build_id, "XML", "./reports", "veracode_")
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
