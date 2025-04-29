# tests/test_utils.py

import unittest
from utils import validate_ip, validate_report_type
from unittest.mock import patch

class TestUtils(unittest.TestCase):

    def test_validate_ip_valid(self):
        """Test that a valid IP address is accepted."""
        valid_ip = "192.168.1.1"
        result = validate_ip(valid_ip)
        self.assertTrue(result)

    def test_validate_ip_invalid(self):
        """Test that an invalid IP address is rejected."""
        invalid_ip = "999.999.999.999"
        result = validate_ip(invalid_ip)
        self.assertFalse(result)

    def test_validate_report_type_valid(self):
        """Test that a valid report type is accepted."""
        valid_report_type = "text"
        result = validate_report_type(valid_report_type)
        self.assertTrue(result)

    def test_validate_report_type_invalid(self):
        """Test that an invalid report type is rejected."""
        invalid_report_type = "docx"
        result = validate_report_type(invalid_report_type)
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
