import subprocess  # nosec
import logging
import re
from nmap_parser import NmapParser  # type: ignore

class Scanner:
    def __init__(self, target):
        if not self._is_valid_target(target):
            raise ValueError(f"Invalid target: {target}")
        self.target = target
        self.logger = logging.getLogger(__name__)
        self.parser = NmapParser()

    def _is_valid_target(self, target):
        # Allow simple domains, IPv4 addresses, or hostnames
        ip_pattern = r"^(\d{1,3}\.){3}\d{1,3}$"
        domain_pattern = r"^[a-zA-Z0-9.-]+$"
        return re.match(ip_pattern, target) or re.match(domain_pattern, target)

    def _run_nmap(self, options):
        """
        Internal helper to run nmap with given options and parse result.
        """
        command = ["nmap"] + options + [self.target]
        self.logger.info(f"Running command: {' '.join(command)}")

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
                shell=False  # Explicitly disable shell
            )
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
