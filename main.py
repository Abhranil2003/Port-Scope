import argparse
import logging
from src.scanner import Scanner
from parsers.nmap_parser import NmapParser
from reporters.csv_reporter import CSVReporter
from reporters.pdf_reporter import PDFReporter
from reporters.html_reporter import HTMLReporter
from reporters.text_reporter import TextReporter
from reporters.json_reporter import JSONReporter  # Added import
from utils import save_raw_output, save_json_output

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

def main():
    parser = argparse.ArgumentParser(description="🔍 Advanced Nmap Scanner & Reporter")
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("-p", "--ports", help="Ports to scan (e.g., 22,80,443)")
    parser.add_argument("-o", "--output", nargs="*", default=["csv"],
                        help="Output formats: csv, pdf, html, text, json")
    parser.add_argument("--raw", action="store_true", help="Save raw Nmap output")
    args = parser.parse_args()

    # Step 1: Perform scan
    scanner = Scanner()
    logger.info(f"🎯 Scanning target: {args.target}")
    nmap_output = scanner.scan(args.target, ports=args.ports)

    # Step 2: Optionally save raw output
    if args.raw:
        save_raw_output(nmap_output, folder="test_reporters")

    # Step 3: Parse output
    parser = NmapParser()
    parsed_data = parser.parse(nmap_output)

    # Step 4: Generate selected reports
    for fmt in args.output:
        fmt = fmt.lower()
        if fmt == "csv":
            CSVReporter(output_dir="test_reporters").generate_report(parsed_data)
        elif fmt == "pdf":
            PDFReporter(output_dir="test_reporters").generate_report(parsed_data)
        elif fmt == "html":
            HTMLReporter(output_dir="test_reporters").generate_report(parsed_data)
        elif fmt == "text":
            TextReporter(output_dir="test_reporters").generate_report(parsed_data)
        elif fmt == "json":
            JSONReporter(output_dir="test_reporters").generate_report(parsed_data)  # Added this line
        else:
            logger.warning(f"⚠️ Unsupported output format: {fmt}")

if __name__ == "__main__":
    main()
