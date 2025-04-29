import argparse
import logging
from scanner import Scanner
from reporter.csv_reporter import CSVReporter
from reporter.pdf_reporter import PDFReporter
from reporter.html_reporter import HTMLReporter
from reporter.text_reporter import TextReporter
from reporter.json_reporter import JSONReporter
from utils import save_raw_output, save_json_output

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

def main():
    parser = argparse.ArgumentParser(description="🔍 Advanced Nmap Scanner & Reporter")
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("-p", "--ports", help="Ports to scan (e.g., 22,80,443)")
    parser.add_argument("-o", "--output", nargs="*", default=["csv"],
                        help="Output formats: csv, pdf, html, text, json")
    parser.add_argument("--scan-type", choices=["quick", "full", "os"], default="full",
                        help="Type of scan to perform (default: full)")
    parser.add_argument("--raw", action="store_true", help="Save raw Nmap output")
    args = parser.parse_args()

    # Step 1: Initialize scanner
    scanner = Scanner(args.target)
    logger.info(f"🎯 Scanning target: {args.target}")

    # Step 2: Choose scan type and get parsed + raw output
    if args.scan_type == "quick":
        scan_result = scanner.quick_scan()
    elif args.scan_type == "os":
        scan_result = scanner.os_detection_scan()
    else:
        scan_result = scanner.full_scan()

    if not scan_result:
        logger.error("❌ Scan failed or returned no data.")
        return

    parsed_data = scan_result["parsed"]

    # Step 3: Optionally save raw Nmap output
    if args.raw:
        save_raw_output(scan_result["raw_output"], folder="logs")

    # Step 4: Generate selected reports
    for fmt in args.output:
        fmt = fmt.lower()
        if fmt == "csv":
            CSVReporter(scanner, output_dir="test_reporters").generate_report(parsed_data)
        elif fmt == "pdf":
            PDFReporter(scanner, output_dir="test_reporters").generate_report(parsed_data)
        elif fmt == "html":
            HTMLReporter(scanner, output_dir="test_reporters").generate_report(parsed_data)
        elif fmt == "text":
            TextReporter(scanner, output_dir="test_reporters").generate_report(parsed_data)
        elif fmt == "json":
            JSONReporter(scanner, output_dir="test_reporters").generate_report(parsed_data)
        else:
            logger.warning(f"⚠️ Unsupported output format: {fmt}")

if __name__ == "__main__":
    main()
