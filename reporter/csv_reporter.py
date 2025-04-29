try:
    import pandas as pd # type: ignore
except ImportError:
    pd = None
    print("⚠️  'pandas' is not installed. CSV report generation will not work.")

from utils import get_output_path

class CSVReporter:
    def __init__(self, scanner):
        self.scanner = scanner

    def generate_report(self, scan_result):
        output_path_csv = get_output_path("reports", "scan_report.csv")

        if pd is None:
            print("⚡ Fallback: 'pandas' not found. Saving as plain text instead of CSV.")
            fallback_path = get_output_path("reports", "scan_report.txt")
            with open(fallback_path, "w") as f:
                f.write(scan_result)
            print(f"✅ Fallback Text report saved at {fallback_path}")
        else:
            data = {"ScanResult": [scan_result]}
            df = pd.DataFrame(data)
            df.to_csv(output_path_csv, index=False)
            print(f"✅ CSV report saved at {output_path_csv}")