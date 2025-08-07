"""Documentation agent."""
from __future__ import annotations

import logging
from pathlib import Path


class DocAgent:
    """Generate documentation for clients based on vars.txt."""

    def __init__(self, vars_file: Path = Path("vars.txt"), output: Path = Path("client.txt")) -> None:
        self.vars_file = vars_file
        self.output = output
        self.logger = logging.getLogger(self.__class__.__name__)

    def run(self) -> None:
        if not self.vars_file.exists():
            self.logger.warning("vars.txt not found; skipping client documentation")
            return
        lines = self.vars_file.read_text().splitlines()
        content = ["Netboot Client Instructions", "===========================", ""]
        content += lines
        self.output.write_text("\n".join(content))
        self.logger.info("Client documentation written to %s", self.output)

