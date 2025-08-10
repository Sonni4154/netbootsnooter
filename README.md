# Netboot Snooter

A modular, agent-driven toolkit for building a self-documenting netboot server. The system is under active development and currently focuses on collecting host network information and hosting boot files.

## Usage
```
python -m netboot.main
```
Generated files:
- `vars.txt`: Detected network variables.
- `client.txt`: Information for netboot clients (stub).
- HTTP and TFTP services serve files from `boot/`.

Logs are stored in `logs/`.

## Development
- Python 3.11
- Run tests with `pytest`
- See `AGENTS.md` for contribution rules.
