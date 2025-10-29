import os
import xml.dom.minidom
from veracode_xml.config import DEFAULT_OUTPUT_DIR, ensure_output_dir

def save_output(content: str, args, task_name: str, ext: str = "xml"):
    """
    Save API response content to a file.
    File name: <prefix><task_name>_<app_id or app_name>.<ext>
    """
    output_dir = ensure_output_dir(getattr(args, "output_dir", DEFAULT_OUTPUT_DIR))
    prefix = getattr(args, "prefix", "")
    identifier = getattr(args, "app_id", getattr(args, "app_name", "output"))

    filename = f"{prefix}{task_name}_{identifier}.{ext}"
    file_path = os.path.join(output_dir, filename)

    with open(file_path, "wb" if ext.lower() == "pdf" else "w", encoding=None if ext.lower() == "pdf" else "utf-8") as f:
        f.write(content)

    print(f"✅ Saved output to {file_path}")
    return file_path

def pretty_print_xml(xml_string: str):
    """
    Pretty-print XML to console.
    """
    try:
        dom = xml.dom.minidom.parseString(xml_string)
        pretty = dom.toprettyxml()
        print(pretty)
    except Exception:
        # fallback if parsing fails
        print(xml_string)
