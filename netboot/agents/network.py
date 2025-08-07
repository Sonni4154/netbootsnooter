"""Network detection agent."""
from __future__ import annotations

import logging
import socket
from pathlib import Path

import netifaces


class NetworkScrapeAgent:
    """Collect network variables and persist them to vars.txt."""

    def __init__(self, output: Path = Path("vars.txt")) -> None:
        self.output = output
        self.logger = logging.getLogger(self.__class__.__name__)

    def run(self) -> dict[str, str]:
        info: dict[str, str] = {}
        hostname = socket.gethostname()
        info["hostname"] = hostname
        fqdn = socket.getfqdn()
        info["fqdn"] = fqdn

        gateways = netifaces.gateways().get('default', {})
        if gateways:
            for fam, gw in gateways.items():
                info[f"gateway_{fam}"] = gw[0]

        interfaces = {}
        for iface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(iface)
            ipv4 = addrs.get(netifaces.AF_INET, [])
            if ipv4:
                interfaces[iface] = ipv4[0].get('addr')
        info["interfaces"] = interfaces

        # DNS servers
        resolv = Path('/etc/resolv.conf')
        if resolv.exists():
            dns = []
            for line in resolv.read_text().splitlines():
                if line.startswith('nameserver'):
                    dns.append(line.split()[1])
            info['dns'] = dns

        self.output.write_text("\n".join(f"{k}={v}" for k, v in info.items()))
        self.logger.info("Network variables written to %s", self.output)
        return info

