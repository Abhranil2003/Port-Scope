import subprocess  # nosec
import logging
import re
import requests
from parsers.nmap_parser import NmapParser  # type: ignore
from bs4 import BeautifulSoup  # type: ignore

class Scanner:
    def __init__(self, target):
        if not self._is_valid_target(target):
            raise ValueError(f"Invalid target: {target}")
        self.target = target
        self.logger = logging.getLogger(__name__)
        self.parser = NmapParser()

    def _is_valid_target(self, target):
        ip_pattern = r"^(\d{1,3}\.){3}\d{1,3}$"
        domain_pattern = r"^[a-zA-Z0-9.-]+$"
        return target.startswith("http://") or target.startswith("https://") or \
               re.match(ip_pattern, target) or re.match(domain_pattern, target)

    def _run_nmap(self, options):
        command = ["nmap"] + options + [self.target]
        self.logger.info(f"Running command: {' '.join(command)}")

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
                shell=False
            )
            raw_output = result.stdout
            parsed = self.parser.parse(raw_output)
            self.logger.info("Scan completed successfully.")
            return {
                "parsed": parsed,
                "raw_output": raw_output
            }
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Scan failed: {e}")
            return None

    def _run_web_scan(self):
        self.logger.info(f"Running web scan for: {self.target}")
        try:
            response = requests.get(self.target, timeout=10)
            raw = f"{response.status_code}\n{response.headers}\n\n{response.text[:1000]}"
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.title.string.strip() if soup.title and soup.title.string else "N/A"

            parsed = {
                "url": self.target,
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "title": title,
                "server": response.headers.get("Server", "N/A"),
                "content_type": response.headers.get("Content-Type", "N/A"),
            }

            return {
                "parsed": parsed,
                "raw_output": raw
            }

        except Exception as e:
            self.logger.error(f"Web scan failed: {e}")
            return None

    def quick_scan(self):
        return self._run_nmap(["-T4", "--top-ports", "10"])

    def full_scan(self):
        return self._run_nmap(["-T4", "-p-", "-sV"])

    def os_detection_scan(self):
        return self._run_nmap(["-O"])

    def custom_scan(self, custom_options):
        return self._run_nmap(custom_options)

    def web_scan(self):
        return self._run_web_scan()
