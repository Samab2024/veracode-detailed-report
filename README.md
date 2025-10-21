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

| Short | Long           | Required                | Description                    | Example                  |
| ----- | -------------- | ----------------------- | ------------------------------ | ------------------------ |
| `-i`  | `--app_id`     | ✅ (either this or `-n`) | Veracode application ID        | `-i 1234567`             |
| `-n`  | `--app_name`   | ✅ (either this or `-i`) | Veracode application name      | `-n "test_app"`         |
| `-f`  | `--format`     | ✅                       | Report format (`XML` or `PDF`) | `-f PDF`                 |
| `-r`  | `--region`     | ❌ (default: `us`)       | Veracode region (`us` or `eu`) | `-r eu`                  |
| `-o`  | `--output_dir` | ❌ (default: `.`)        | Output directory for report    | `-o ~/Downloads/reports` |
| `-p`  | `--prefix`     | ❌ (default: `""`)       | Optional filename prefix       | `-p test_`               |
| `-h`  | `--help`       | ❌                       | Show help text                 | `-h`                     |

Examples

Fetch an XML report by app ID (US region)
By app_id
veracode-report -i 1234567 -f XML

By app_name
veracode-report -n "test_app" -f PDF -o ~/Downloads -p test_

Fetch a PDF report by app name (EU region)
veracode-report -n "My App EU" -f PDF -r eu -o ~/Downloads/ -p test_

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
