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

```bash
git clone https://github.com/<your-username>/veracode-detailed-report.git
cd veracode-detailed-report
pip install -r requirements.txt
pip install .
