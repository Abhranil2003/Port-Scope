import logging
from datetime import datetime
try:
    import pandas as pd  # type: ignore
except ImportError:
    pd = None
    print("⚠️ 'pandas' is not installed. CSV report generation will not work.")

from utils import ensure_directory, get_output_path

class CSVReporter:
    def __init__(self, scanner, output_dir="reports"):
        self.scanner = scanner
        self.output_dir = ensure_directory(output_dir)
        self.logger = logging.getLogger(__name__)

    def generate_report(self, parsed_data):
        if not parsed_data:
            self.logger.error("No data provided for CSV report generation.")
            return None

        filename = f"scan_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = get_output_path(self.output_dir, filename)

        try:
            open_ports = parsed_data.get("open_ports", [])
            if not open_ports:
                open_ports = [{"port": "None", "protocol": "", "service": ""}]

            if pd is None:
                self.logger.warning("Pandas not available. Cannot generate CSV.")
                return None

            df = pd.DataFrame(open_ports)
            df["target"] = parsed_data.get("target", "")
            df["scan_date"] = parsed_data.get("scan_date", "")
            df.to_csv(filepath, index=False)

            self.logger.info(f"CSV report generated: {filepath}")
            return filepath
        except Exception as e:
            self.logger.error(f"Failed to generate CSV report: {e}")
            return None
