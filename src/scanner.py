import subprocess
import logging
from nmap_parser import NmapParser

class Scanner:
    def __init__(self, target):
        self.target = target
        self.logger = logging.getLogger(__name__)
        self.parser = NmapParser()

    def _run_nmap(self, options):
        """
        Internal helper to run nmap with given options and parse result.
        """
        command = ["nmap"] + options + [self.target]
        self.logger.info(f"Running command: {' '.join(command)}")

        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            self.logger.info("Scan completed successfully.")
            return self.parser.parse(result.stdout)
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Scan failed: {e}")
            return None

    def quick_scan(self):
        return self._run_nmap(["-T4", "--top-ports", "10"])

    def full_scan(self):
        return self._run_nmap(["-T4", "-p-", "-sV"])

    def os_detection_scan(self):
        return self._run_nmap(["-O"])

    def custom_scan(self, custom_options):
        return self._run_nmap(custom_options)
