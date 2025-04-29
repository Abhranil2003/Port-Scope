import os

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

def get_sample_report_path(filename):
    return get_output_path("sample_reports", filename)

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
