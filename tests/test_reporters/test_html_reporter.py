import unittest
from reporters.html_reporter import HTMLReporter

class TestHTMLReporter(unittest.TestCase):

    def setUp(self):
        self.reporter = HTMLReporter(target="test_target", scan_type="quick")

    def test_generate_report_with_customization(self):
        """Test HTML report with custom fields (e.g., scan time)."""
        custom_fields = {"Scan Time": "2025-04-29 14:00:00", "User": "Admin"}
        self.reporter.generate_report("scan result", custom_fields)
        output = self.reporter.output.getvalue()
        self.assertIn("<html>", output)
        self.assertIn("Scan Time: 2025-04-29 14:00:00", output)
        self.assertIn("User: Admin", output)

    def test_generate_report_with_invalid_input(self):
        """Test HTML reporter with invalid input."""
        with self.assertRaises(ValueError):
            self.reporter.generate_report(None)

if __name__ == "__main__":
    unittest.main()
