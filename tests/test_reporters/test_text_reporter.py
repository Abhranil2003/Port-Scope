import unittest
from reporters.text_reporter import TextReporter

class TestTextReporter(unittest.TestCase):

    def setUp(self):
        self.reporter = TextReporter(target="test_target", scan_type="quick")

    def test_generate_report_with_special_characters(self):
        """Test that the text report is generated correctly with special characters."""
        special_characters = "!@#$%^&*()_+[]{}|;:,.<>?"
        self.reporter.generate_report(special_characters)
        output = self.reporter.output.getvalue()
        self.assertIn("Scan Report for test_target", output)
        self.assertIn("Scan Type: quick", output)
        self.assertIn(special_characters, output)

    def test_generate_report_with_invalid_input(self):
        """Test text reporter with invalid input."""
        with self.assertRaises(ValueError):
            self.reporter.generate_report(None)

if __name__ == "__main__":
    unittest.main()
