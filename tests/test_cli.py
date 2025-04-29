# tests/test_cli.py

import unittest
from cli import main
from unittest.mock import patch
import sys

class TestCLI(unittest.TestCase):

    @patch("sys.argv", ["cli.py", "192.168.1.1", "quick", "--report-type", "text"])
    @patch("builtins.print")
    def test_cli_quick_scan(self, mock_print):
        """Test CLI for quick scan."""
        main()
        mock_print.assert_called_with("Running quick scan on 192.168.1.1 and generating text report.")

    @patch("sys.argv", ["cli.py", "192.168.1.1", "full", "--report-type", "csv"])
    @patch("builtins.print")
    def test_cli_full_scan(self, mock_print):
        """Test CLI for full scan."""
        main()
        mock_print.assert_called_with("Running full scan on 192.168.1.1 and generating csv report.")

    @patch("sys.argv", ["cli.py", "192.168.1.1", "os-detection", "--report-type", "pdf"])
    @patch("builtins.print")
    def test_cli_os_detection(self, mock_print):
        """Test CLI for OS detection scan."""
        main()
        mock_print.assert_called_with("Running OS detection scan on 192.168.1.1 and generating pdf report.")

    @patch("sys.argv", ["cli.py", "192.168.1.1", "custom", "--report-type", "html", "--custom-options", "-p", "80,443"])
    @patch("builtins.print")
    def test_cli_custom_scan(self, mock_print):
        """Test CLI for custom scan."""
        main()
        mock_print.assert_called_with("Running custom scan on 192.168.1.1 with options: -p 80,443 and generating html report.")

    @patch("sys.argv", ["cli.py", "192.168.1.1", "quick", "--invalid-option", "value"])
    @patch("builtins.print")
    def test_cli_invalid_option(self, mock_print):
        """Test CLI for invalid option."""
        with self.assertRaises(SystemExit):
            main()

if __name__ == "__main__":
    unittest.main()
