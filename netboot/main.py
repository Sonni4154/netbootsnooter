"""Entry point for running agents."""
from __future__ import annotations

import logging
from pathlib import Path

from .agents.network import NetworkScrapeAgent
from .agents.doc_agent import DocAgent

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


if __name__ == "__main__":
    main()

