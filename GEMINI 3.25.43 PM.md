# Artemis City GEMINI.md

This document provides a comprehensive overview of the Artemis City project, its architecture, and development practices, intended for use by AI assistants and new developers.

## Project Overview

Artemis City is an architectural framework for creating and managing AI agents. It emphasizes transparent, accountable, and secure interactions between agents and with external systems. The project's philosophy is detailed in the `codex/manifesto.md` file, which outlines principles like "Iterative Clarity," "Net Good Over Noise," and "Transparent Accountability."

The project is a hybrid system:

* **Python:** The core agent framework, CLI, and agent definitions are written in Python.
* **Node.js/TypeScript:** A service named "Artemis Agentic Memory Layer" is built with Node.js, Express, and TypeScript. This service acts as a "Model Context Protocol (MCP) server for Obsidian vaults," providing a REST API to interact with a knowledge base.

### Key Components

* **Agents:** The system is composed of several agents, each with a specific role and set of keywords. These are defined in `src/interface/agent_router.yaml`. The current agents are:
  * `artemis`: Governance and policy.
  * `pack_rat`: Secure data transfer.
  * `codex_daemon`: System status and memory interface.
  * `copilot`: Contextual assistance.
* **CLI:** The primary user interface is a command-line interface (`src/interface/codex_cli.py`) that can be run interactively or used to execute single commands.
* **Memory Layer:** The Node.js service provides a memory and knowledge base for the agents, integrating with Obsidian.
* **Personas:** Agents have "personas" (e.g., `src/agents/artemis/persona.py`) that define their communication style and response patterns, making them more interactive and conversational.
* **Artemis Transmission Protocol (ATP):** A structured communication protocol for agents.

## Building and Running

### Python Environment

1. **Create and activate a virtual environment:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

2. **Install dependencies:**

    ```bash
    pip install -r src/launch/requirements.txt
    ```

    For development, install the dev dependencies:

    ```bash
    pip install -r src/launch/requirements-dev.txt
    ```

### Node.js Environment (Memory Layer)

1. **Navigate to the memory layer directory:**

    ```bash
    cd "src/Artemis Agentic Memory Layer"
    ```

2. **Install dependencies:**

    ```bash
    npm install
    ```

### Running the Application

1. **Start the Memory Layer server:**

    ```bash
    cd "src/Artemis Agentic Memory Layer"
    npm run dev
    ```

2. **Run the Python CLI (in a separate terminal):**

    ```bash
    source .venv/bin/activate
    python src/interface/codex_cli.py
    ```

    You can also run the CLI with the `artemis` command after installing the project in editable mode (`pip install -e .`).

## Development Conventions

### Python

* **Formatting:** The project uses `black` for code formatting and `isort` for import sorting.
* **Linting:** `flake8` and `pylint` are used for linting.
* **Type Checking:** `mypy` is used for static type checking.
* **Testing:** `pytest` is the testing framework. Tests are located in the `tests/` directory.
* **Security:** `bandit` and `safety` are used for security scanning.

### Node.js/TypeScript

* **Linting:** `eslint` is used for linting.
* **Build:** The TypeScript code is compiled to JavaScript using `tsc`.

### CI/CD

The project has a comprehensive CI/CD pipeline in `.github/workflows/ci.yml` that automates formatting, linting, testing, and security scanning for both the Python and Node.js code.

### Key Files

* `README.md`: The main entry point for understanding the project.
* `pyproject.toml`: Python project configuration and dependencies.
* `src/interface/codex_cli.py`: The main entry point for the Python CLI.
* `src/Artemis Agentic Memory Layer/package.json`: Node.js project configuration and dependencies.
* `src/interface/agent_router.yaml`: Defines the agents and their keywords for routing commands.
* `src/agents/artemis/persona.py`: An example of an agent's persona, defining its communication style.
* `tests/`: Contains the Python tests.
* `.github/workflows/ci.yml`: The CI/CD pipeline definition.
* `docs/`: Contains additional documentation about the project's features and architecture.
* `SECURITY.md`: Outlines the security best practices for the project.
