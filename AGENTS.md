# Repository Guidelines

## Project Structure & Module Organization
- `src/` — core Python code. Key areas: `agents/` (personas, ATP parsing), `integration/` (memory client, postal service demo), `interface/` (CLI entry at `interface/codex_cli.py`), `sandbox_city/` (simulated environments), `launch/` (memory-layer Node service).
- `tests/` — pytest suite covering ATP, memory integration, instruction loading, and persona behaviors.
- `docs/` — supplementary guides and setup scripts (e.g., `docs/setup_secrets.sh`).
- `dist/` — build artifacts; treat as generated. `node_modules/` is vendored for the launch service.

## Build, Test, and Development Commands
- Create env and install deps:  
  ```bash
  python -m venv .venv && source .venv/bin/activate
  pip install -e '.[dev]'
  ```
- Run CLI locally: `python main.py` (or `python main.py "ask artemis about system status"`).
- Start memory-layer service (if needed):  
  ```bash
  cd src/launch && npm install && npm run dev
  ```
- Run demos: `python demo_city_postal.py`, `python demo_memory_integration.py`, `python demo_artemis.py`.
- Test suite:  
  ```bash
  pytest tests/ -v
  pytest tests/ -v --cov=. --cov-report=html
  ```

## Coding Style & Naming Conventions
- Python: 4-space indent, 100-char lines (`.editorconfig`). Prefer double quotes; keep imports sorted via isort (Black profile). Run Black for formatting.
- Linting: flake8 config in `src/.flake8` (relaxed ignores for tests/sandbox). Keep cyclomatic complexity ≤10 where practical.
- JS/TS (launch service): 2-space indent, single quotes, 100-char lines.
- Naming: modules and files are snake_case; classes are PascalCase; functions/vars are snake_case; tests use `test_<unit>.py`.

## Testing Guidelines
- Framework: pytest; entry point `tests/` (see `tests/TEST_PLAN.md` for scenarios).
- Aim to keep new tests near related modules (mirrored paths under `tests/`).
- Use parametrized tests for protocol cases; prefer fixture reuse to avoid duplicated setup.
- Include coverage when changing protocol parsing, persona logic, or memory integration.

## Commit & Pull Request Guidelines
- Commit style follows conventional types (see history: `refactor: ...`). Use lowercase type + colon + concise scope, e.g., `feat: add atp edge-case coverage`.
- PRs should include: summary of changes, linked issues (if any), test evidence (`pytest`/coverage output), and notes on affected demos or memory-layer steps. Add screenshots only when UI/simulation output is relevant.

## Security & Configuration Tips
- Never commit secrets or `.env` files; ensure generated env files stay gitignored. Use `docs/setup_secrets.sh` if you need to scaffold secrets locally.
- Keep the memory-layer service isolated; do not expose it publicly. Validate new integrations against sandbox scripts in `sandbox_city/` before touching live endpoints.
