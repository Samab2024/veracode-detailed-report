# 🧩 Veracode XML CLI

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Veracode API](https://img.shields.io/badge/veracode-xml--api-orange)](https://docs.veracode.com/r/c_api_main)

A unified and modular **CLI tool** for interacting with the [Veracode XML APIs](https://docs.veracode.com/r/c_api_main) —  
fetch detailed reports, builds, and more — all secured with **HMAC authentication**.

---

## 🚀 Features
- 🧱 Modular task-based design (e.g. `detailed_report`, `summary`, etc.)
- 🔄 Supports both **Static (SS)** and **Dynamic (DS)** scan types
- 📥 Auto-detects latest build for selected app
- 📂 Download reports in **XML** or **PDF**
- 🌍 Supports US, EU, and Gov regions
- 🧩 Clean structure and reusable modules

---

## ⚙️ Installation

```bash
git clone https://github.com/Samab2024/veracode-xml.git
cd veracode-xml
pip install -r requirements.txt
pip install .
```

---

## 🧠 CLI Usage
```
veracode-xml -t detailed_report --app_name "My App" --format PDF \
    --scan_type ds --output_dir ~/Downloads --prefix myapp_
```
Parameters
```
| Short | Long           | Required                 | Description                    | Example                  |
| ----- | -------------- | ------------------------ | ------------------------------ | ------------------------ |
| `-t`  | `--task`       | ✅                       | Veracode Action XML            | `-t detailed_report`     |
| `-i`  | `--app_id`     | ✅ (either this or `-n`) | Veracode application ID        | `-i 1234567`             |
| `-n`  | `--app_name`   | ✅ (either this or `-i`) | Veracode application name      | `-n "test_app"`          |
| `-f`  | `--format`     | ✅                       | Report format (`XML` or `PDF`) | `-f PDF`                 |
| `-r`  | `--region`     | ❌ (default: `us`)       | Veracode region (`us` or `eu`) | `-r eu`                  |
| `-o`  | `--output_dir` | ❌ (default: `.`)        | Output directory for report    | `-o ~/Downloads/reports` |
| `-p`  | `--prefix`     | ❌ (default: `""`)       | Optional filename prefix       | `-p test_`               |
| `-s`  | `--scan_type`  | ❌ (default: `ss`)       | Optional scan type             | `-s ds`                  |
| `-h`  | `--help`       | ❌                       | Show help text                 | `-h`                     |
```

---

## 📘 Examples
```
🔹 Get Static Scan Report (XML)

veracode-xml -t detailed_report -n "Core Banking App" -f XML -s ss

🔸 Get Dynamic Scan Report (PDF)

veracode-xml -t detailed_report -n "Customer Portal" -f PDF -s ds \
  -o ~/Downloads -p dyn_
```

---

## 🔐 Authentication
```
Store your Veracode HMAC credentials securely in:

~/.veracode/credentials

ini
Copy code
[default]
veracode_api_key_id = YOUR_KEY_ID
veracode_api_key_secret = YOUR_KEY_SECRET
Your credentials are automatically loaded using the Veracode Python HMAC library.
```

---

## 🧱 Project Structure
```
veracode_xml/
├── __init__.py
├── cli.py                  # CLI entry point
├── config.py               # API endpoint and region config
├── tasks/
│   ├── __init__.py
│   └── detailed_report.py  # First supported task
└── utils/
    ├── __init__.py
    └── api_helpers.py      # Common HMAC + API XML logic
```

---

## 🧩 Adding New Tasks
```
Each task lives inside the tasks/ folder and exposes a run(args) function.

Example (tasks/my_new_task.py):

def run(args):
    print(f"Running new task: {args.task}")
Then invoke:

veracode-xml -t my_new_task
```

---

## 🧪 Development Setup
```
# From project root
python -m veracode_xml.cli -t detailed_report -n "My App" -f XML -s ds

Or install in editable mode:

pip install -e .
```

---

## 🪪 License

MIT License © 2025 Samab2024

```
Note:
This tool is not affiliated with Veracode and is intended for automation and reporting purposes using their public APIs.
