import os
import logging
from datetime import datetime
import pdfkit  # type: ignore
from jinja2 import Environment, FileSystemLoader, select_autoescape
from utils import ensure_directory, get_output_path

class PDFReporter:
    def __init__(self, scanner, output_dir="reports", template_dir=None):
        self.scanner = scanner
        self.output_dir = ensure_directory(output_dir)

        # Set template and assets directories
        base_dir = os.path.dirname(__file__)
        self.template_dir = os.path.join(base_dir, "templates") if template_dir is None else template_dir
        self.assets_dir = os.path.join(base_dir, "assets")
        self.logger = logging.getLogger(__name__)

        # Windows-specific wkhtmltopdf configuration
        wkhtmltopdf_path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        self.pdf_config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

    def generate_report(self, parsed_data):
        if not parsed_data:
            self.logger.error("No data provided for PDF report generation.")
            return None

        env = Environment(
            loader=FileSystemLoader([self.template_dir, self.assets_dir]),  # support template + local assets
            autoescape=select_autoescape(['html', 'xml'])
        )
        template = env.get_template("report_template.html")
        html_content = template.render(parsed_data=parsed_data)

        filename = f"scan_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = get_output_path(self.output_dir, filename)

        try:
            pdfkit.from_string(html_content, filepath, configuration=self.pdf_config)
            self.logger.info(f"PDF report generated: {filepath}")
            return filepath
        except Exception as e:
            self.logger.error(f"Failed to generate PDF report: {e}")
            return None
