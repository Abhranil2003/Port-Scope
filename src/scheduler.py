import threading
import time
import logging

class Scheduler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def schedule_scan(self, scan_function, delay_seconds, *args, **kwargs):
        """
        Schedule a one-time scan after a certain delay.

        Args:
            scan_function (callable): The scan function to call.
            delay_seconds (int): Number of seconds to wait before executing.
            *args: Arguments to pass to scan_function.
            **kwargs: Keyword arguments to pass to scan_function.
        """
        def delayed_scan():
            self.logger.info(f"🕒 Waiting {delay_seconds} seconds before starting scan...")
            time.sleep(delay_seconds)
            self.logger.info(f"🚀 Starting scheduled scan now!")
            try:
                scan_function(*args, **kwargs)
                self.logger.info("✅ Scan completed successfully.")
            except Exception as e:
                self.logger.error(f"❌ Scheduled scan failed: {e}")

        thread = threading.Thread(target=delayed_scan)
        thread.start()
        return thread

    def schedule_repeated_scan(self, scan_function, interval_seconds, repetitions, *args, **kwargs):
        """
        Schedule a scan to repeat multiple times at regular intervals.

        Args:
            scan_function (callable): The scan function to call.
            interval_seconds (int): Number of seconds between each execution.
            repetitions (int): How many times to repeat the scan.
            *args: Arguments to pass to scan_function.
            **kwargs: Keyword arguments to pass to scan_function.
        """
        def repeated_scan():
            for i in range(repetitions):
                self.logger.info(f"🚀 Running scheduled scan #{i+1}/{repetitions}")
                try:
                    scan_function(*args, **kwargs)
                    self.logger.info(f"✅ Scan #{i+1} completed successfully.")
                except Exception as e:
                    self.logger.error(f"❌ Repeated scan #{i+1} failed: {e}")
                if i < repetitions - 1:
                    self.logger.info(f"🕒 Waiting {interval_seconds} seconds for next scan...")
                    time.sleep(interval_seconds)

        thread = threading.Thread(target=repeated_scan)
        thread.start()
        return thread
