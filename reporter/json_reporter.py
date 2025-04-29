import os
import json
import logging
from datetime import datetime

class JSONReporter:
    def __init__(self, output_dir="reports"):
        self.output_dir = output_dir
        self.logger = logging.getLogger(__name__)
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_report(self, parsed_data):
        """
        Generates and saves a JSON report from parsed scan data.
        :param parsed_data: Dictionary output from NmapParser.parse()
        :return: Path to the saved JSON report
        """
        if not parsed_data:
            self.logger.error("No data provided for JSON report generation.")
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scan_report_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)

        try:
            with open(filepath, 'w') as jsonfile:
                json.dump(parsed_data, jsonfile, indent=4)
            self.logger.info(f"✅ JSON report generated: {filepath}")
            return filepath
        except Exception as e:
            self.logger.error(f"❌ Failed to generate JSON report: {e}")
            return None
