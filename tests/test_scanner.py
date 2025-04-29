# tests/test_scanner.py

import unittest
from scanner import Scanner
from unittest.mock import patch

class TestScanner(unittest.TestCase):

    def setUp(self):
        """Called before every test."""
        self.target = "192.168.1.1"
        self.scanner = Scanner(self.target)

    @patch("subprocess.run")
    def test_quick_scan(self, mock_run):
        """Test the quick scan functionality."""
        mock_run.return_value.stdout = "Quick scan completed"
        result = self.scanner.quick_scan()
        self.assertEqual(result, "Quick scan completed")
        mock_run.assert_called_with(["nmap", "-T4", "-F", self.target], capture_output=True, text=True, check=True)

    @patch("subprocess.run")
    def test_full_scan(self, mock_run):
        """Test the full scan functionality."""
        mock_run.return_value.stdout = "Full scan completed"
        result = self.scanner.full_scan()
        self.assertEqual(result, "Full scan completed")
        mock_run.assert_called_with(["nmap", "-p-", "-T4", "-v", self.target], capture_output=True, text=True, check=True)

    @patch("subprocess.run")
    def test_os_detection_scan(self, mock_run):
        """Test the OS detection scan functionality."""
        mock_run.return_value.stdout = "OS detection completed"
        result = self.scanner.os_detection_scan()
        self.assertEqual(result, "OS detection completed")
        mock_run.assert_called_with(["nmap", "-O", "-T4", self.target], capture_output=True, text=True, check=True)

    @patch("subprocess.run")
    def test_custom_scan(self, mock_run):
        """Test the custom scan functionality."""
        mock_run.return_value.stdout = "Custom scan completed"
        custom_options = ["-p", "80,443"]
        result = self.scanner.custom_scan(custom_options)
        self.assertEqual(result, "Custom scan completed")
        mock_run.assert_called_with(["nmap", "-p", "80,443", self.target], capture_output=True, text=True, check=True)

if __name__ == "__main__":
    unittest.main()
