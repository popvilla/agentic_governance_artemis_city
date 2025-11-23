# Contributing to Artemis City

Thank you for your interest in contributing to Artemis City! This document provides guidelines for maintaining code quality and consistency.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Code Style Guidelines](#code-style-guidelines)
3. [Linting and Formatting](#linting-and-formatting)
4. [Pre-commit Hooks](#pre-commit-hooks)
5. [Testing](#testing)
6. [Pull Request Process](#pull-request-process)

## Getting Started

### Setup Development Environment

```bash
# Clone the repository
git clone <repository-url>
cd Artemis-City

# Setup secrets
./setup_secrets.sh

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
make setup-hooks
# or: pip install pre-commit && pre-commit install
```

### Quick Commands

```bash
make help          # Show all available commands
make lint          # Run linters
make format        # Auto-format code
make check         # Run all checks
make security      # Security scans
make test          # Run tests
```

## Code Style Guidelines

### Python Style

We follow **PEP 8** with modifications for modern Python development:

**Line Length:**

- Maximum: 100 characters (not 79)
- Docstrings/comments: Can wrap naturally

**Naming Conventions:**

- Functions/variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private: `_leading_underscore`
- Project-specific abbreviations: `mcp`, `atp`, `id`, `db`

**Docstrings:**

- Use Google-style docstrings
- Required for all public functions/classes
- Include Args, Returns, Raises sections

```python
def example_function(param1: str, param2: int) -> bool:
    """Brief description of function.
    
    Longer description if needed. Can span multiple lines
    and provide detailed context.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param2 is negative
    """
    if param2 < 0:
        raise ValueError("param2 must be non-negative")
    return True
```

**Imports:**

```python
# Standard library
import os
import sys
from typing import Dict, List

# Third-party
import yaml

# Local application
from agents.atp import ATPParser
from memory.integration import MemoryClient
```

### TypeScript/JavaScript Style

**Formatting:**

- Use **Prettier** for formatting
- Line length: 100 characters
- Indentation: 2 spaces
- Single quotes for strings
- Semicolons required
- Trailing commas (ES5)

**Naming Conventions:**

- Variables/functions: `camelCase`
- Classes/Types: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private: `_prefixedUnderscore` or `#private`

### File Organization

**Python Files:**

```python
"""Module docstring describing the file's purpose."""

# Imports (grouped and sorted)
import standard_library
import third_party
import local_modules

# Constants
CONSTANT_VALUE = "value"

# Classes
class MyClass:
    pass

# Functions
def my_function():
    pass

# Main execution
if __name__ == "__main__":
    main()
```

## Linting and Formatting

### Automatic Formatting

**Format all Python code:**

```bash
make format
# or
black .
isort .
```

**Format JavaScript/TypeScript:**

```bash
cd "Artemis Agentic Memory Layer "
npm run lint:fix
```

### Linting Tools

#### Python

**Flake8** - Style guide enforcement:

```bash
flake8 .
```

**Pylint** - Comprehensive static analysis:

```bash
pylint agents/ core/ interface/ memory/
```

**MyPy** - Type checking:

```bash
mypy .
```

**Bandit** - Security scanner:

```bash
bandit -r . -c pyproject.toml
```

#### JavaScript/TypeScript

**ESLint** (if configured):

```bash
cd "Artemis Agentic Memory Layer "
npm run lint
```

### Configuration Files

Our linting configuration:

- `.flake8` - Flake8 settings
- `.pylintrc` - Pylint settings
- `pyproject.toml` - Black, isort, Bandit, pytest settings
- `.prettierrc` - Prettier settings
- `.editorconfig` - Editor consistency
- `.gitattributes` - Line endings and file handling

## Pre-commit Hooks

We use **pre-commit** to automatically check code before commits.

### Installation

```bash
pip install pre-commit
pre-commit install
```

### What Gets Checked

Pre-commit hooks run automatically on `git commit`:

 **File Checks:**

- Large files (>1MB)
- Line endings (LF)
- Trailing whitespace
- YAML/JSON syntax

 **Python Checks:**

- Black formatting
- isort import sorting
- Flake8 linting
- Bandit security scanning

 **Secret Detection:**

- Private key detection
- Secret pattern matching
- .env file prevention

 **JavaScript/TypeScript:**

- Prettier formatting
- Markdown linting

### Usage

**Run manually on all files:**

```bash
pre-commit run --all-files
```

**Skip hooks (emergency only):**

```bash
git commit --no-verify
```

**Update hooks:**

```bash
pre-commit autoupdate
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=. --cov-report=html

# Specific test file
pytest tests/test_agent.py -v

# Using Make
make test
make test-cov
```

### Writing Tests

**Test file structure:**

```python
"""Tests for module_name."""

import pytest
from module_name import function_to_test


class TestClassName:
    """Tests for ClassName."""
    
    def test_basic_functionality(self):
        """Test basic functionality."""
        result = function_to_test()
        assert result == expected_value
    
    def test_error_handling(self):
        """Test error handling."""
        with pytest.raises(ValueError):
            function_to_test(invalid_input)
```

**Test naming:**

- Files: `test_*.py` or `*_test.py`
- Functions: `test_*`
- Classes: `Test*`

## Pull Request Process

### Before Submitting

1. **Run all checks:**

   ```bash
   make check
   make security
   make test
   ```

2. **Format your code:**

   ```bash
   make format
   ```

3. **Update documentation:**
   - Update docstrings
   - Update README.md if needed
   - Add to CHANGELOG.md

4. **Verify pre-commit passes:**

   ```bash
   pre-commit run --all-files
   ```

### PR Requirements

 **Code Quality:**

- All linters pass
- No security issues
- Type hints for public APIs
- Docstrings for public functions

 **Testing:**

- Tests pass
- New features have tests
- Coverage doesn't decrease

 **Documentation:**

- Code is documented
- README updated if needed
- Breaking changes noted

 **Git:**

- Commits are descriptive
- Branch is up to date
- No merge conflicts

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added new tests
- [ ] Manual testing done

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings
```

## Code Review Guidelines

### For Authors

- Keep PRs focused and small
- Write clear commit messages
- Respond to feedback promptly
- Update PR based on reviews

### For Reviewers

- Be constructive and respectful
- Focus on code, not person
- Explain reasoning
- Approve when standards met

## Security Guidelines

**Never commit:**

- API keys or tokens
- Passwords or credentials
- Private keys
- `.env` files (except `.env.example`)
- Personal data

**Use:**

- Environment variables for secrets
- `.env.example` as template
- `setup_secrets.sh` for setup

**Check before committing:**

```bash
make secrets
```

## Additional Resources

- [Python PEP 8](https://pep8.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Black Documentation](https://black.readthedocs.io/)
- [Flake8 Rules](https://www.flake8rules.com/)
- [Pre-commit Hooks](https://pre-commit.com/)

## ❓ Questions?

- Check [README.md](README.md) for project overview
- See [SECURITY.md](SECURITY.md) for security practices
- Read [WARP.md](WARP.md) for AI assistant guidelines
- Open an issue for questions

---

**Thank you for contributing to Artemis City!**
