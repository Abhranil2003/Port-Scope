import os
import json
from datetime import datetime

def ensure_directory(path):
    """
    Ensures that the specified directory exists.
    If it does not exist, creates it.
    """
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def sanitize_filename(filename):
    """
    Sanitize a filename by replacing forbidden characters.
    """
    return "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_')).rstrip()

def get_output_path(output_dir, filename):
    """
    Constructs and returns a full output path for the report file.
    """
    ensure_directory(output_dir)
    sanitized_filename = sanitize_filename(filename)
    return os.path.join(output_dir, sanitized_filename)

def get_sample_report_path(filename, folder="sample_reports"):
    """
    Constructs path for sample reports stored in a dedicated folder.
    """
    ensure_directory(folder)
    return os.path.join(folder, sanitize_filename(filename))

def human_readable_time(seconds):
    """
    Converts seconds into a more human-readable HH:MM:SS format.
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

def banner_text():
    """
    Returns a fancy banner for the CLI tool.
    """
    return """
    ================================================
    ||       Welcome to Port Scanner Pro!         ||
    ||     Powered by Python + Nmap + Magic!       ||
    ================================================
    """

def validate_ip_address(ip):
    """
    Basic IP address validation.
    """
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    for item in parts:
        if not item.isdigit() or not 0 <= int(item) <= 255:
            return False
    return True

def save_raw_output(output, folder="logs"):
    """
    Saves raw Nmap output to a timestamped .txt file.
    """
    ensure_directory(folder)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"nmap_raw_{timestamp}.txt"
    path = get_output_path(folder, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(output)
    return path

def save_json_output(data, folder="logs"):
    """
    Saves parsed data to a timestamped JSON file.
    """
    ensure_directory(folder)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"nmap_report_{timestamp}.json"
    path = get_output_path(folder, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return path
