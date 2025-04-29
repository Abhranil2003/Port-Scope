import os
from datetime import datetime
import logging

class TextReporter:
    def __init__(self, output_dir="reports"):
        self.output_dir = output_dir
        self.logger = logging.getLogger(__name__)
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_report(self, parsed_data):
        """
        Generates and saves a plain text report from parsed scan data.
        :param parsed_data: Dictionary output from NmapParser.parse()
        :return: Path to the saved report
        """
        if not parsed_data:
            self.logger.error("No data provided for report generation.")
            return None

        report_lines = []
        report_lines.append(f"Scan Report - {parsed_data.get('scan_date', 'Unknown')}")
        report_lines.append("=" * 50)
        report_lines.append(f"Target: {parsed_data.get('target', 'Unknown')}")
        report_lines.append("")

        report_lines.append("Open Ports:")
        open_ports = parsed_data.get("open_ports", [])
        if open_ports:
            for port_info in open_ports:
                line = f" - Port {port_info['port']}/{port_info['protocol']} ({port_info['service']})"
                report_lines.append(line)
        else:
            report_lines.append(" - No open ports found.")
        report_lines.append("")

        report_lines.append("OS Detection:")
        os_info = parsed_data.get("os_info", ["Not detected"])
        for info in os_info:
            report_lines.append(f" - {info}")
        report_lines.append("=" * 50)

        # Create report filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scan_report_{timestamp}.txt"
        filepath = os.path.join(self.output_dir, filename)

        # Save report
        try:
            with open(filepath, 'w') as f:
                f.write("\n".join(report_lines))
            self.logger.info(f"Text report generated: {filepath}")
            return filepath
        except Exception as e:
            self.logger.error(f"Failed to save report: {e}")
            return None
