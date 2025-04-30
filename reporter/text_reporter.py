import os
from datetime import datetime
import logging
from utils import ensure_directory, get_output_path

class TextReporter:
    def __init__(self, scanner, output_dir="reports"):
        self.scanner = scanner
        self.output_dir = ensure_directory(output_dir)
        self.logger = logging.getLogger(__name__)

    def generate_report(self, parsed_data):
        if not parsed_data:
            self.logger.error("No data provided for report generation.")
            return None

        report_lines = []
        report_lines.append(f"Scan Report - {parsed_data.get('scan_date', 'Unknown')}")
        report_lines.append("=" * 50)
        report_lines.append(f"Target: {parsed_data.get('target', 'Unknown')}\n")

        report_lines.append("Open Ports:")
        open_ports = parsed_data.get("open_ports", [])
        if open_ports:
            for port_info in open_ports:
                report_lines.append(f" - Port {port_info['port']}/{port_info['protocol']} ({port_info['service']})")
        else:
            report_lines.append(" - No open ports found.")
        report_lines.append("")

        report_lines.append("OS Detection:")
        os_info = parsed_data.get("os_info", ["Not detected"])
        for info in os_info:
            report_lines.append(f" - {info}")
        report_lines.append("=" * 50)

        filename = f"scan_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = get_output_path(self.output_dir, filename)

        try:
            with open(filepath, 'w') as f:
                f.write("\n".join(report_lines))
            self.logger.info(f"Text report generated: {filepath}")
            return filepath
        except Exception as e:
            self.logger.error(f"Failed to save report: {e}")
            return None
