import unittest
from reporters.csv_reporter import CSVReporter

class TestCSVReporter(unittest.TestCase):

    def setUp(self):
        self.reporter = CSVReporter(target="test_target", scan_type="full")

    def test_generate_report_with_large_data(self):
        """Test that the CSV report is generated correctly with a large number of results."""
        large_data = ["Result {}".format(i) for i in range(1000)]  # Simulate 1000 scan results
        self.reporter.generate_report(large_data)
        output = self.reporter.output.getvalue()
        self.assertGreater(len(output), 1000)  # Ensure the output is large enough
        self.assertIn("Target", output)
        self.assertIn("Scan Type", output)

    def test_generate_report_with_invalid_input(self):
        """Test CSV reporter with invalid input."""
        with self.assertRaises(ValueError):
            self.reporter.generate_report(None)

if __name__ == "__main__":
    unittest.main()
