import re
import logging
from datetime import datetime

class NmapParser:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def parse(self, nmap_output):
        """
        Parses nmap output and returns structured data.
        :param nmap_output: Raw output string from nmap scan.
        :return: Dictionary with scan data.
        """
        if not nmap_output:
            self.logger.error("Empty Nmap output provided to parser.")
            return {}

        try:
            parsed_data = {
                "scan_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "target": self._extract_target(nmap_output),
                "open_ports": self._extract_open_ports(nmap_output),
                "os_info": self._extract_os_info(nmap_output),
            }

            self.logger.info("Successfully parsed Nmap scan output.")
            return parsed_data

        except Exception as e:
            self.logger.error(f"Exception occurred while parsing Nmap output: {e}")
            return {}

    def _extract_target(self, nmap_output):
        """Extracts target IP/hostname from output."""
        match = re.search(r"Nmap scan report for (.+)", nmap_output)
        if match:
            target = match.group(1)
            self.logger.debug(f"Target extracted: {target}")
            return target
        else:
            self.logger.warning("Target not found in Nmap output.")
            return "Unknown"

    def _extract_open_ports(self, nmap_output):
        """Extracts open ports and services."""
        open_ports = []
        port_line_pattern = re.compile(r"(\d+/tcp|\d+/udp)\s+open\s+(\S+)")
        matches = port_line_pattern.findall(nmap_output)

        for port_proto, service in matches:
            try:
                port, proto = port_proto.split('/')
                port_info = {
                    "port": int(port),
                    "protocol": proto,
                    "service": service
                }
                open_ports.append(port_info)
                self.logger.debug(f"Open port found: {port_info}")
            except ValueError:
                self.logger.warning(f"Invalid port line format: {port_proto} {service}")

        if not open_ports:
            self.logger.info("No open ports detected.")

        return open_ports

    def _extract_os_info(self, nmap_output):
        """Attempts to extract OS details if available."""
        os_info = []
        capture = False

        for line in nmap_output.splitlines():
            if "OS details:" in line:
                os_info.append(line.strip())
            elif "Aggressive OS guesses" in line:
                capture = True
            elif capture:
                if line.strip() == "":
                    capture = False
                else:
                    os_info.append(line.strip())

        if os_info:
            self.logger.debug(f"OS info extracted: {os_info}")
        else:
            os_info = ["Not detected"]
            self.logger.info("No OS information detected.")

        return os_info
