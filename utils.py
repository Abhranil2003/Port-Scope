import os

SAFE_NMAP_OPTIONS = {
    "-sS", "-sT", "-sU", "-sV", "-O", "-Pn", "-T1", "-T2", "-T3", "-T4", "-T5",
    "-p", "-F", "--top-ports", "-v", "-vv", "-A", "--reason", "--osscan-guess"
}

def ensure_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def sanitize_filename(filename):
    return "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_')).rstrip()

def get_output_path(output_dir, filename):
    ensure_directory(output_dir)
    sanitized_filename = sanitize_filename(filename)
    return os.path.join(output_dir, sanitized_filename)

def human_readable_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

def banner_text():
    return """
    ================================================
    ||       Welcome to Port Scanner Pro!         ||
    ||     Powered by Python + Nmap + Magic!       ||
    ================================================
    """

def validate_ip_address(ip):
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    for item in parts:
        if not item.isdigit() or not 0 <= int(item) <= 255:
            return False
    return True

def get_sample_report_path(filename):
    path = os.path.join("sample_reports", filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Sample report '{filename}' not found.")
    return path

def save_raw_output(output, folder="logs"):
    ensure_directory(folder)
    path = os.path.join(folder, "nmap_raw_output.txt")
    with open(path, "w") as f:
        f.write(output)

def save_json_output(parsed_data, folder="logs"):
    import json
    ensure_directory(folder)
    path = os.path.join(folder, "nmap_parsed_output.json")
    with open(path, "w") as f:
        json.dump(parsed_data, f, indent=2)

def sanitize_custom_options(options):
    """
    Sanitizes a list of custom Nmap options by allowing only a known safe subset.
    Returns a filtered list. Raises ValueError on invalid or dangerous input.
    """
    sanitized = []
    for opt in options:
        if opt in SAFE_NMAP_OPTIONS or opt.startswith("-p") or opt.startswith("--top-ports"):
            sanitized.append(opt)
        else:
            raise ValueError(f"❌ Unsafe or unsupported Nmap option: {opt}")
    return sanitized
