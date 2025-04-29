# tests/test_parser.py

import unittest
from parser import parse_args
from unittest.mock import patch
import sys

class TestParser(unittest.TestCase):

    @patch("sys.argv", ["cli.py", "192.168.1.1", "quick", "--report-type", "text"])
    def test_parse_args_quick_scan(self):
        """Test parsing of arguments for a quick scan."""
        args = parse_args()
        self.assertEqual(args.target, "192.168.1.1")
        self.assertEqual(args.scan_type, "quick")
        self.assertEqual(args.report_type, "text")

    @patch("sys.argv", ["cli.py", "192.168.1.1", "full", "--report-type", "csv"])
    def test_parse_args_full_scan(self):
        """Test parsing of arguments for a full scan."""
        args = parse_args()
        self.assertEqual(args.target, "192.168.1.1")
        self.assertEqual(args.scan_type, "full")
        self.assertEqual(args.report_type, "csv")

    @patch("sys.argv", ["cli.py", "192.168.1.1", "os-detection", "--report-type", "pdf"])
    def test_parse_args_os_detection(self):
        """Test parsing of arguments for OS detection scan."""
        args = parse_args()
        self.assertEqual(args.target, "192.168.1.1")
        self.assertEqual(args.scan_type, "os-detection")
        self.assertEqual(args.report_type, "pdf")

    @patch("sys.argv", ["cli.py", "192.168.1.1", "custom", "--report-type", "html", "--custom-options", "-p", "80,443"])
    def test_parse_args_custom_scan(self):
        """Test parsing of arguments for custom scan with options."""
        args = parse_args()
        self.assertEqual(args.target, "192.168.1.1")
        self.assertEqual(args.scan_type, "custom")
        self.assertEqual(args.report_type, "html")
        self.assertEqual(args.custom_options, ["-p", "80,443"])

    @patch("sys.argv", ["cli.py", "192.168.1.1", "quick", "--report-type", "text", "--invalid-option", "value"])
    def test_parse_args_invalid_option(self):
        """Test that an invalid argument is handled gracefully."""
        with self.assertRaises(SystemExit):
            parse_args()

if __name__ == "__main__":
    unittest.main()
