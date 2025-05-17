import argparse
import logging
from scanner import Scanner
from scheduler import Scheduler
from reporters.text_reporter import TextReporter
from reporters.csv_reporter import CSVReporter
from reporters.pdf_reporter import PDFReporter
from reporters.html_reporter import HTMLReporter
from reporters.json_reporter import JSONReporter
from utils import get_sample_report_path, sanitize_custom_options

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Port Scanner CLI Tool")
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("scan_type", choices=["quick", "full", "os", "custom"], help="Type of scan to perform")
    parser.add_argument("-c", "--custom-options", help="Custom Nmap options as a comma-separated string", default="")
    parser.add_argument("-r", "--report-type", choices=["text", "csv", "pdf", "html", "json"], help="Report format", default="text")
    parser.add_argument("--schedule", action="store_true", help="Schedule the scan to run after a delay")
    parser.add_argument("--delay", type=int, default=10, help="Delay in seconds before starting the scan (for scheduled scan)")
    parser.add_argument("--repeated", action="store_true", help="Schedule the scan to run multiple times (repeated scan)")
    parser.add_argument("--interval", type=int, default=60, help="Interval in seconds between repeated scans")
    parser.add_argument("--repetitions", type=int, default=3, help="Number of times to repeat the scan")
    parser.add_argument("--sample-report", help="Name of sample report to generate from sample_reports directory")

    args = parser.parse_args()

    if args.sample_report:
        path = get_sample_report_path(args.sample_report)
        print(f"✅ Sample report path: {path}")
        return

    scanner = Scanner(args.target)
    scheduler = Scheduler()

    if args.report_type == "text":
        reporter = TextReporter(scanner)
    elif args.report_type == "csv":
        reporter = CSVReporter(scanner)
    elif args.report_type == "pdf":
        reporter = PDFReporter(scanner)
    elif args.report_type == "html":
        reporter = HTMLReporter(scanner)
    elif args.report_type == "json":
        reporter = JSONReporter(scanner)

    scan_function = None
    if args.scan_type == "quick":
        scan_function = scanner.quick_scan
    elif args.scan_type == "full":
        scan_function = scanner.full_scan
    elif args.scan_type == "os":
        scan_function = scanner.os_detection_scan
    elif args.scan_type == "custom":
        custom_options = args.custom_options.split(",") if args.custom_options else []
        try:
            safe_options = sanitize_custom_options(custom_options)
            scan_function = lambda: scanner.custom_scan(safe_options)
        except ValueError as ve:
            print(str(ve))
            return

    if args.schedule:
        scheduler.schedule_scan(scan_function, delay_seconds=args.delay)
    elif args.repeated:
        scheduler.schedule_repeated_scan(scan_function, interval_seconds=args.interval, repetitions=args.repetitions)
    else:
        result = scan_function()
        if result:
            reporter.generate_report(result)

if __name__ == "__main__":
    main()
