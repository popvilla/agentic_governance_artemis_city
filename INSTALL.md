#  Installation Guide

This guide covers all methods for installing and setting up Artemis City.

##  Prerequisites

- **Python**: 3.8+ (3.13+ recommended)
- **Node.js**: 18+ (for Memory Layer)
- **Git**: For cloning the repository
- **Obsidian**: With Local REST API plugin (for memory features)

##  Quick Install

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Artemis-City
```

### 2. Secure Environment Setup

**Automated (Recommended):**
```bash
./setup_secrets.sh
```

**Manual:**
```bash
cp .env.example .env
openssl rand -hex 32  # Generate API key
# Edit .env and add the generated key as MCP_API_KEY
chmod 600 .env
```

### 3. Install Python Dependencies

**Using pip (standard):**
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

**Using uv (faster):**
```bash
pip install uv
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

**Using poetry:**
```bash
poetry install
```

### 4. Install Memory Layer (Node.js)

```bash
cd "Artemis Agentic Memory Layer "
npm install
cd ..
```

### 5. Verify Installation

```bash
# Test Python CLI
python interface/codex_cli.py "help"

# Test demos (requires MCP server running)
python demo_artemis.py
```

##  Installation Methods

### Method 1: Standard pip

**Basic installation:**
```bash
pip install -r requirements.txt
```

**With development tools:**
```bash
pip install -r requirements-dev.txt
```

**With optional features:**
```bash
pip install -r requirements.txt
pip install pydantic requests rich  # Enhanced features
```

### Method 2: uv (Fast Package Manager)

```bash
# Install uv
pip install uv

# Create virtual environment and install
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Or one-liner
uv pip install -r requirements.txt
```

### Method 3: Poetry

```bash
# Install poetry
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# With optional extras
poetry install --extras "dev docs enhanced"

# Activate environment
poetry shell
```

### Method 4: pyproject.toml (Modern)

```bash
# Install in development mode
pip install -e .

# With optional dependencies
pip install -e ".[dev]"        # Development tools
pip install -e ".[docs]"       # Documentation
pip install -e ".[enhanced]"   # Enhanced features
pip install -e ".[dev,docs]"   # Multiple extras
```

##  Installation Profiles

### Minimal (Core Only)
**Just run the CLI and basic features:**
```bash
pip install pyyaml>=6.0.1
```

### Standard (Recommended)
**Everything you need for regular use:**
```bash
pip install -r requirements.txt
```

### Developer
**Full development environment:**
```bash
pip install -r requirements-dev.txt
```

### Production
**Optimized for deployment:**
```bash
pip install --no-dev -r requirements.txt
```

##  Security Configuration

### Environment Variables

Create `.env` files in both locations:

**Root `.env`:**
```bash
MCP_BASE_URL=http://localhost:3000
MCP_API_KEY=your_generated_key_here
OBSIDIAN_BASE_URL=http://localhost:27124
OBSIDIAN_API_KEY=your_obsidian_key_here
```

**Memory Layer `.env`:**
```bash
cd "Artemis Agentic Memory Layer "
cp .env.example .env
# Edit with same MCP_API_KEY as root .env
```

### Generate Secure Keys

```bash
# Using openssl
openssl rand -hex 32

# Using Python
python -c "import secrets; print(secrets.token_hex(32))"

# Using Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

### File Permissions

```bash
chmod 600 .env
chmod 600 "Artemis Agentic Memory Layer /.env"
```

##  Verify Installation

### Check Python Environment

```bash
# Verify Python version
python --version  # Should be 3.8+

# List installed packages
pip list | grep -i yaml  # Should show pyyaml 6.0.1+

# Check import
python -c "import yaml; print(yaml.__version__)"
```

### Check Node Environment

```bash
cd "Artemis Agentic Memory Layer "

# Verify Node version
node --version  # Should be 18+

# Verify npm packages
npm list --depth=0

# Test build
npm run build
```

### Run Tests

```bash
# CLI test
python interface/codex_cli.py "help"

# Module import test
python -c "from agents.atp import ATPParser; print('ATP OK')"
python -c "from memory.integration import MemoryClient; print('Memory OK')"

# Full demo (requires MCP server)
python demo_artemis.py
```

##  Starting Services

### Start Everything

**Terminal 1 - MCP Server:**
```bash
cd "Artemis Agentic Memory Layer "
npm run dev
```

**Terminal 2 - Artemis CLI:**
```bash
source .venv/bin/activate
python interface/codex_cli.py
```

### Alternative: Single Command

```bash
# Run CLI directly (without interactive mode)
python interface/codex_cli.py "ask artemis about system status"
```

## 🐳 Docker Installation (Optional)

If you prefer Docker:

```bash
cd "Artemis Agentic Memory Layer "

# Build
docker-compose build

# Run
docker-compose up

# Or detached
docker-compose up -d
```

##  Updating

### Update Python Dependencies

```bash
# Pull latest changes
git pull

# Update packages
pip install -r requirements.txt --upgrade

# Or with uv
uv pip install -r requirements.txt --upgrade
```

### Update Node Dependencies

```bash
cd "Artemis Agentic Memory Layer "
npm update
npm audit fix  # Fix security issues
```

##  Uninstall

### Remove Virtual Environment

```bash
# Deactivate first
deactivate

# Remove directory
rm -rf .venv
```

### Remove Node Modules

```bash
cd "Artemis Agentic Memory Layer "
rm -rf node_modules
rm package-lock.json
```

### Remove Configuration

```bash
# Remove environment files (BE CAREFUL!)
rm .env
rm "Artemis Agentic Memory Layer /.env"

# Remove cache
rm -rf __pycache__
rm -rf **/__pycache__
rm -rf .pytest_cache
```

## ❓ Troubleshooting

### Python Issues

**Problem: `ModuleNotFoundError: No module named 'yaml'`**
```bash
# Solution: Install PyYAML
pip install pyyaml>=6.0.1
```

**Problem: Virtual environment not activating**
```bash
# Solution: Create new venv
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Node Issues

**Problem: `Cannot find module 'express'`**
```bash
# Solution: Reinstall node_modules
cd "Artemis Agentic Memory Layer "
rm -rf node_modules package-lock.json
npm install
```

**Problem: Port 3000 already in use**
```bash
# Solution: Use different port
PORT=3001 npm run dev
```

### Memory Layer Issues

**Problem: MCP server connection failed**
```bash
# Check server is running
curl http://localhost:3000/health

# Check environment variables
echo $MCP_API_KEY
echo $MCP_BASE_URL
```

**Problem: Obsidian API connection failed**
```bash
# Verify Obsidian Local REST API plugin is:
# 1. Installed
# 2. Enabled
# 3. API key generated and in .env
```

##  Next Steps

After installation:

1.  Read **[SECURITY.md](SECURITY.md)** - Security best practices
2.  Read **[README.md](README.md)** - Project overview
3.  Try **demos** - Run demo scripts to test features
4.  Configure **Obsidian** - Set up Local REST API plugin
5.  Explore **agents** - Review agent definitions in `agents/`

##  Getting Help

- Check **[README.md](README.md)** for usage examples
- Review **[WARP.md](WARP.md)** for development guide
- Check **[SECURITY.md](SECURITY.md)** for security questions
- Open an issue on GitHub for bugs or questions

---

**Installation complete!**  Your Artemis City is ready for secure development!
