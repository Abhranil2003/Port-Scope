# tests/test_scheduler.py

import unittest
from scheduler import Scheduler
from unittest.mock import MagicMock

class TestScheduler(unittest.TestCase):

    def setUp(self):
        """Called before every test."""
        self.scheduler = Scheduler()

    def test_schedule_scan(self):
        """Test the schedule_scan method."""
        mock_scan_function = MagicMock(return_value="Scan completed")
        # Scheduling a scan with a 1-second delay
        thread = self.scheduler.schedule_scan(mock_scan_function, 1)
        # Simulating that the scan finishes
        thread.join()  # This ensures the scheduled task finishes
        mock_scan_function.assert_called_once()

    def test_schedule_repeated_scan(self):
        """Test the schedule_repeated_scan method."""
        mock_scan_function = MagicMock(return_value="Scan completed")
        # Scheduling a repeated scan for 3 times with 1-second interval
        thread = self.scheduler.schedule_repeated_scan(mock_scan_function, 1, 3)
        thread.join()  # Ensure all repetitions finish
        self.assertEqual(mock_scan_function.call_count, 3)

if __name__ == "__main__":
    unittest.main()
