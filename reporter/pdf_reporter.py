import os
import logging
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
from utils import ensure_directory, get_output_path
from weasyprint import HTML  # ✅ WeasyPrint used instead of pdfkit

class PDFReporter:
    def __init__(self, scanner, output_dir="reports", template_dir=None):
        self.scanner = scanner
        self.output_dir = ensure_directory(output_dir)
        base_dir = os.path.dirname(__file__)
        self.template_dir = os.path.join(base_dir, "templates") if template_dir is None else template_dir
        self.logger = logging.getLogger(__name__)

    def generate_report(self, parsed_data):
        if not parsed_data:
            self.logger.error("No data provided for PDF report generation.")
            return None

        # Render HTML from Jinja2 template
        env = Environment(
            loader=FileSystemLoader(self.template_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )
        template = env.get_template("report_template.html")
        html_content = template.render(parsed_data=parsed_data)

        # Save rendered HTML to a temporary file (optional, for debugging)
        filename = f"scan_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        output_path = get_output_path(self.output_dir, filename)

        try:
            # ✅ Generate PDF using WeasyPrint
            HTML(string=html_content, base_url=self.template_dir).write_pdf(output_path)
            self.logger.info(f"PDF report generated: {output_path}")
            return output_path
        except Exception as e:
            self.logger.error(f"Failed to generate PDF report: {e}")
            return None
