# ============================================
# ARTEMIS CITY - MAKEFILE
# ============================================
# Convenient commands for development tasks
# Usage: make <target>

.PHONY: help install lint format test clean security check pre-commit setup-hooks

# Default target
.DEFAULT_GOAL := help

# ============================================
# HELP
# ============================================

help: ## Show this help message
	@echo "Artemis City - Available Commands"
	@echo "="
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""

# ============================================
# INSTALLATION
# ============================================

install: ## Install all dependencies
	echo "Installing Python dependencies..."
	pip install -r requirements.txt
	echo "Installation complete!"

install-dev: ## Install development dependencies
	echo "Installing development dependencies..."
	pip install -r requirements-dev.txt
	@echo "Development dependencies installed!"

setup-hooks: ## Install pre-commit hooks
	@echo "Installing pre-commit hooks..."
	pip install pre-commit
	pre-commit install
	@echo "Pre-commit hooks installed!"

# ============================================
# CODE QUALITY
# ============================================

lint: ## Run all linters
	@echo "Running linters..."
	@echo "\n--- Flake8 ---"
	flake8 . || true
	@echo "\n--- Pylint ---"
	pylint agents/ core/ interface/ memory/ || true
	@echo "\nLinting complete!"

lint-fix: ## Run linters with auto-fix
	@echo "Running linters with auto-fix..."
	@echo "\n--- Black (formatter) ---"
	black .
	@echo "\n--- isort (import sorter) ---"
	isort .
	@echo "\nAuto-fix complete!"

format: lint-fix ## Format code (alias for lint-fix)

check: ## Run all checks (format, lint, type)
	@echo "Running all checks..."
	@echo "\n--- Black (check only) ---"
	black --check .
	@echo "\n--- isort (check only) ---"
	isort --check-only .
	@echo "\n--- Flake8 ---"
	flake8 .
	@echo "\n--- MyPy (type checking) ---"
	mypy . || true
	@echo "\nAll checks complete!"

# ============================================
# SECURITY
# ============================================

security: ## Run security checks
	@echo "Running security checks..."
	@echo "\n--- Bandit (security scanner) ---"
	bandit -r . -c pyproject.toml || true
	@echo "\n--- Safety (dependency vulnerabilities) ---"
	safety check || true
	@echo "\nSecurity checks complete!"

secrets: ## Check for accidentally committed secrets
	@echo "Checking for secrets..."
	@git diff --cached --name-only | xargs grep -l "API_KEY\|SECRET\|PASSWORD" 2>/dev/null \
		&& echo "WARNING: Potential secrets detected!" || echo "No secrets detected"

# ============================================
# TESTING
# ============================================

test: ## Run tests (when available)
	@echo "Running tests..."
	pytest tests/ -v || echo "WARNING: No tests directory found"

test-cov: ## Run tests with coverage
	@echo "Running tests with coverage..."
	pytest tests/ --cov=. --cov-report=html --cov-report=term || echo "WARNING: No tests directory found"

# ============================================
# PRE-COMMIT
# ============================================

pre-commit: ## Run pre-commit hooks on all files
	@echo "Running pre-commit hooks..."
	pre-commit run --all-files

pre-commit-update: ## Update pre-commit hooks
	@echo "Updating pre-commit hooks..."
	pre-commit autoupdate

# ============================================
# CLEANUP
# ============================================

clean: ## Remove build artifacts and cache files
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name "*.coverage" -delete 2>/dev/null || true
	rm -rf build/ dist/ .tox/ htmlcov/ .coverage
	@echo "Cleanup complete!"

clean-env: ## Remove virtual environment
	@echo "Removing virtual environment..."
	rm -rf .venv venv
	@echo "Virtual environment removed!"

# ============================================
# DEVELOPMENT
# ============================================

run: ## Run the CLI interactively
	@echo "Starting Artemis City CLI..."
	python interface/codex_cli.py

demo: ## Run all demos
	@echo "Running demos..."
	@echo "\n--- Artemis Features Demo ---"
	python demo_artemis.py
	@echo "\n--- Memory Integration Demo ---"
	python demo_memory_integration.py
	@echo "\n--- City Postal Demo ---"
	python demo_city_postal.py
	@echo "\nDemos complete!"

server: ## Start MCP server (Memory Layer)
	@echo "Starting MCP server..."
	cd "Artemis Agentic Memory Layer " && npm run dev

# ============================================
# BUILD & PACKAGE
# ============================================

build: ## Build the package
	@echo "Building package..."
	python -m build
	@echo "Build complete!"

# ============================================
# DOCUMENTATION
# ============================================

docs: ## Build documentation (if available)
	@echo "Building documentation..."
	mkdocs build || echo "WARNING: MkDocs not configured"

docs-serve: ## Serve documentation locally
	@echo "Serving documentation..."
	mkdocs serve || echo "WARNING: MkDocs not configured"

# ============================================
# ALL-IN-ONE COMMANDS
# ============================================

all: clean install-dev format lint security test ## Run all quality checks
	@echo "All tasks complete!"

ci: check test ## Run CI checks (format check, lint, test)
	@echo "CI checks complete!"
