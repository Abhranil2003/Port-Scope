import os
import logging
from datetime import datetime
from playwright.sync_api import sync_playwright
from jinja2 import Environment, FileSystemLoader, select_autoescape
from utils import ensure_directory, get_output_path

class PDFReporter:
    def __init__(self, scanner, output_dir="reports", template_dir=None):
        self.scanner = scanner
        self.output_dir = ensure_directory(output_dir)
        self.template_dir = template_dir or os.path.join(os.path.dirname(__file__), "templates")
        self.logger = logging.getLogger(__name__)

    def generate_report(self, parsed_data):
        if not parsed_data:
            self.logger.error("No data provided for PDF report generation.")
            return None

        # Render HTML using Jinja2
        env = Environment(
            loader=FileSystemLoader(self.template_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )
        template = env.get_template("report_template.html")
        html_content = template.render(parsed_data=parsed_data)

        # Save HTML temporarily
        filename = f"scan_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        html_path = get_output_path(self.output_dir, f"{filename}.html")
        pdf_path = get_output_path(self.output_dir, f"{filename}.pdf")

        try:
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(f"file://{os.path.abspath(html_path)}")
                page.pdf(path=pdf_path, format="A4")
                browser.close()

            self.logger.info(f"✅ PDF report generated: {pdf_path}")
            return pdf_path
        except Exception as e:
            self.logger.error(f"❌ Failed to generate PDF report with Playwright: {e}")
            return None
