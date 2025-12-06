---
tags:
  - "#Python"
  - "#typescript"
  - "#DevOps"
  - "#SoftwareEngineering"
  - "#Infrastructure"
  - "#DevTools"
  - "#AI"
  - "#MachineLearning"
  - "#repository-guidelines"
  - "#coding-style"
  - "#testing-guidelines"
---
# Repository Guidelines

## Project Structure & Module Organization

- Python core in `src/`: `agents/` (personas, ATP), `codex/` (principles), `interface/codex_cli.py` (CLI), `launch/main.py` (runner), and `sandbox_city/` (simulation assets).
- TypeScript MCP server lives in `src/src/` and compiles to `dist/`; configuration sits in `tsconfig.json` and `package.json`.
- Tests are under `tests/` with markers for unit/integration/e2e; docs and indices live in `docs/` and `_Index_*` files.
- Supporting tooling: Docker/Docker Compose for the MCP server, and `setup_secrets.sh` for local .env setup.

## Build, Test, and Development Commands

- Python setup: `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt` (add `pip install -e .[dev]` for tooling).
- Run the CLI: `PYTHONPATH=src python -m interface.codex_cli` or `python src/launch/main.py`; demos are available via `python demo_*.py`.
- TypeScript MCP server: `npm install`, `npm run dev` (nodemon + ts-node), `npm run build` (tsc to `dist`), `npm start` (runs built server). Docker option: `docker-compose up --build` once env vars are set.
- Lint/format: `black .`, `isort .`, `flake8`, `mypy src`; JS/TS lint via `npm run lint`.

## Coding Style & Naming Conventions

- Python: Black-style 4-space indent, line length 100, imports sorted with isort; type hints and concise docstrings for public functions/classes.
- Pytest naming: files `test_*.py`, classes `Test*`, functions `test_*_<scenario>`; shared fixtures belong in `tests/conftest.py` when added.
- TypeScript: ES2020 target, strict mode, 2-space indent; PascalCase classes and camelCase functions/variables; edit sources in `src/src/` only (never `dist/`).

## Testing Guidelines

- Framework: pytest (see `pytest.ini` markers `unit`, `integration`, `e2e`, `slow`, `requires_server`); run `pytest` or `pytest -m "not slow"` for a quick pass.
- Coverage goal: `pytest --cov=. --cov-fail-under=85`.
- Integration tests that touch the MCP server should note required services/env vars and prefer deterministic, small fixtures.

## Commit & Pull Request Guidelines

- Commits follow Conventional Commits (e.g., `feat: ...`, `fix: ...`, `docs: ...`) as seen in recent history.
- For every PR: run formatters, linters, and tests for both Python and TS stacks; include a short summary, linked issue, and screenshots/logs for UX/API changes.
- Surface any security-impacting changes and required env vars. Generate `.env` files via `./setup_secrets.sh` and never commit secrets; refer to `SECURITY.md` for hardening practices.

## Security & Configuration Notes

- Run `./setup_secrets.sh` once to create `.env` files with correct permissions.
- Set MCP env vars (`PORT`, `MCP_API_KEY`, `OBSIDIAN_BASE_URL`, `OBSIDIAN_API_KEY`, `MCP_LOG_LEVEL`) locally or in Docker Compose before starting services.
