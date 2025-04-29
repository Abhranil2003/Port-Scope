import unittest
import time
from reporters.pdf_reporter import PDFReporter

class TestPDFReporter(unittest.TestCase):

    def setUp(self):
        self.reporter = PDFReporter(target="test_target", scan_type="full")

    def test_generate_report_performance(self):
        """Test performance of PDF report generation with large data."""
        large_data = ["Result {}".format(i) for i in range(1000)]
        start_time = time.time()
        self.reporter.generate_report(large_data)
        elapsed_time = time.time() - start_time
        self.assertLess(elapsed_time, 2)  # Ensure report is generated in less than 2 seconds

    def test_generate_report_with_invalid_input(self):
        """Test PDF reporter with invalid input."""
        with self.assertRaises(ValueError):
            self.reporter.generate_report(None)

if __name__ == "__main__":
    unittest.main()
