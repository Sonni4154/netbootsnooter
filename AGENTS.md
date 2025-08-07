# AGENTS

This repository follows a modular agent-based workflow. Each agent is responsible for a specific part of the system and must leave the workspace in a clean, tested state before handover.

## General Rules
- Use Python 3.11 style with type hints where reasonable.
- Keep commits small and semantic (`feat:`, `fix:`, `chore:`).
- Document every decision in commit messages or `PROBLEMS.md`.
- Run `pytest` before committing.
- Log actions to files in `logs/` when the code runs.

## Agent Responsibilities
- **NetworkScrapeAgent**: detect host network parameters and write them to `vars.txt`.
- **DocAgent**: generate user-facing documentation such as `client.txt` based on collected data.
- Future agents should extend this pattern by adding modules under `netboot/agents/` and registering them in `main.py`.

