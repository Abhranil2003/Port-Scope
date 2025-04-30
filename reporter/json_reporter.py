import os
import json
import logging
from datetime import datetime
from utils import ensure_directory, get_output_path

class JSONReporter:
    def __init__(self, scanner, output_dir="reports"):
        self.scanner = scanner
        self.output_dir = ensure_directory(output_dir)
        self.logger = logging.getLogger(__name__)

    def generate_report(self, parsed_data):
        if not parsed_data:
            self.logger.error("No data provided for JSON report generation.")
            return None

        filename = f"scan_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = get_output_path(self.output_dir, filename)

        try:
            with open(filepath, 'w') as jsonfile:
                json.dump(parsed_data, jsonfile, indent=4)
            self.logger.info(f"✅ JSON report generated: {filepath}")
            return filepath
        except Exception as e:
            self.logger.error(f"❌ Failed to generate JSON report: {e}")
            return None
