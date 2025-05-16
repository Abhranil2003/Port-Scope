import argparse
from scanner import Scanner
from scheduler import Scheduler
from reporter.text_reporter import TextReporter
from reporter.csv_reporter import CSVReporter
from reporter.pdf_reporter import PDFReporter
from reporter.html_reporter import HTMLReporter
from reporter.json_reporter import JSONReporter
from parsers.nmap_parser import NmapParser  
from utils import get_sample_report_path

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
    parser_instance = NmapParser()  

    if args.report_type == "text":
        reporter = TextReporter(scanner)
    elif args.report_type == "csv":
        reporter = CSVReporter(scanner)
    elif args.report_type == "pdf":
        reporter = PDFReporter(scanner)
    elif args.report_type == "html":
        reporter = HTMLReporter(scanner)
    elif args.report_type == "json":
        reporter = JSONReporter()

    if args.scan_type == "quick":
        scan_function = scanner.quick_scan
    elif args.scan_type == "full":
        scan_function = scanner.full_scan
    elif args.scan_type == "os":
        scan_function = scanner.os_detection_scan
    elif args.scan_type == "custom":
        custom_options = args.custom_options.split(",") if args.custom_options else []
        scan_function = lambda: scanner.custom_scan(custom_options)

    def scheduled_scan_job():
        raw_output = scan_function()
        if raw_output:
            parsed_data = parser_instance.parse(raw_output)
            reporter.generate_report(parsed_data)

    if args.schedule:
        thread = scheduler.schedule_scan(scheduled_scan_job, delay_seconds=args.delay)
        thread.join()

    elif args.repeated:
        thread = scheduler.schedule_repeated_scan(scheduled_scan_job, interval_seconds=args.interval, repetitions=args.repetitions)
        thread.join()

    else:
        raw_output = scan_function()
        if raw_output:
            parsed_data = parser_instance.parse(raw_output)
            reporter.generate_report(parsed_data)

if __name__ == "__main__":
    main()
