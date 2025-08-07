from pathlib import Path

from netboot.agents.network import NetworkScrapeAgent


def test_network_agent_writes_file(tmp_path: Path):
    out = tmp_path / "vars.txt"
    agent = NetworkScrapeAgent(output=out)
    info = agent.run()
    assert out.exists()
    assert "hostname" in info
