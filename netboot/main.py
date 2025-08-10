"""Entry point for running agents."""
from __future__ import annotations

import logging
import time
from pathlib import Path

from .agents.network import NetworkScrapeAgent
from .agents.doc_agent import DocAgent
from .agents.boot_server import BootServerAgent

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "run.log"),
        logging.StreamHandler(),
    ],
)


def main() -> None:
    net_agent = NetworkScrapeAgent()
    info = net_agent.run()
    logging.getLogger("main").info("Detected hostname %s", info.get("hostname"))

    doc_agent = DocAgent()
    doc_agent.run()

    boot_agent = BootServerAgent()
    boot_agent.run()
    try:
        while True:
            time.sleep(60)
            boot_agent.ensure_running()
    except KeyboardInterrupt:
        boot_agent.stop()


if __name__ == "__main__":
    main()

