import os
import logging
from datetime import datetime
from jinja2 import Environment, FileSystemLoader # type: ignore
from utils import ensure_directory, get_output_path

class HTMLReporter:
    def __init__(self, scanner, output_dir="reports", template_dir="templates"):
        self.scanner = scanner
        self.output_dir = ensure_directory(output_dir)
        self.template_dir = template_dir
        self.logger = logging.getLogger(__name__)

    def generate_report(self, parsed_data):
        if not parsed_data:
            self.logger.error("No data provided for HTML report generation.")
            return None

        env = Environment(loader=FileSystemLoader(self.template_dir))
        template = env.get_template("report_template.html")
        html_content = template.render(parsed_data=parsed_data)
        filename = f"scan_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        filepath = get_output_path(self.output_dir, filename)

        try:
            with open(filepath, 'w') as f:
                f.write(html_content)
            self.logger.info(f"HTML report generated: {filepath}")
            return filepath
        except Exception as e:
            self.logger.error(f"Failed to generate HTML report: {e}")
            return None