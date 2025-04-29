import os
import json
import unittest
from reporters.json_reporter import JSONReporter # type: ignore

class TestJSONReporter(unittest.TestCase):
    def setUp(self):
        # Setup mock data similar to what NmapParser would return
        self.parsed_data = {
            "scan_date": "2025-04-29 15:30:00",
            "target": "192.168.0.1",
            "open_ports": [
                {"port": 22, "protocol": "tcp", "service": "ssh"},
                {"port": 80, "protocol": "tcp", "service": "http"}
            ],
            "os_info": ["Linux 3.X", "Ubuntu"]
        }
        self.reporter = JSONReporter(output_dir="test_reports")

    def test_generate_report_creates_json_file(self):
        filepath = self.reporter.generate_report(self.parsed_data)
        self.assertIsNotNone(filepath, "The filepath returned should not be None")
        self.assertTrue(os.path.exists(filepath), "The JSON file should exist at the given path")

        # Check if file contents match the input
        with open(filepath, "r") as f:
            content = json.load(f)

        self.assertEqual(content["target"], self.parsed_data["target"])
        self.assertEqual(content["open_ports"], self.parsed_data["open_ports"])
        self.assertEqual(content["os_info"], self.parsed_data["os_info"])

        # Cleanup
        os.remove(filepath)

    def tearDown(self):
        # Remove the test_reports directory if empty
        if os.path.exists("test_reports") and not os.listdir("test_reports"):
            os.rmdir("test_reports")

if __name__ == "__main__":
    unittest.main()
