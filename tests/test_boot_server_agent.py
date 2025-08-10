import time
import urllib.request
from pathlib import Path

from netboot.agents.boot_server import BootServerAgent


def test_http_server_serves_file_and_self_heals(tmp_path: Path):
    root = tmp_path / "root"
    root.mkdir()
    (root / "index.txt").write_text("hello")
    agent = BootServerAgent(root=root, http_port=0, tftp_port=0)
    port = agent.start_http()
    # allow server to start
    time.sleep(0.1)
    data = urllib.request.urlopen(f"http://127.0.0.1:{port}/index.txt").read().decode()
    assert data == "hello"
    agent.stop_http()
    assert agent.http_thread is None or not agent.http_thread.is_alive()
    agent.ensure_running()
    assert agent.http_thread is not None and agent.http_thread.is_alive()
    agent.stop()
