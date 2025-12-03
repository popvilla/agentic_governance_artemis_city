# GEMINI.md: AI Assistant Guide for Artemis-City

This document provides a comprehensive guide for AI assistants working with the Artemis-City codebase. It outlines the project's architecture, development workflows, and core concepts to ensure effective and consistent collaboration.

## Project Overview

Artemis-City is a sophisticated framework for building and managing distributed agentic systems. It combines a Python-based agent kernel with a Node.js/TypeScript memory layer, enabling agents to reason, communicate, and interact with a persistent knowledge base stored in an Obsidian vault.

The project's mission is to facilitate "net good over noise" by enabling transparent, accountable, and collaborative action among AI agents.

### Core Technologies

*   **Python:** The core agent framework, including the kernel, agent router, and agent implementations.
*   **Node.js/TypeScript:** The "Artemis Agentic Memory Layer" (MCP Server), which provides a REST API for interacting with the Obsidian vault.
*   **Obsidian:** A powerful knowledge base used for persistent agent memory.
*   **Docker:** For containerizing and orchestrating the MCP server.
*   **Pytest:** For testing the Python components.
*   **Hatch:** For building and managing the Python project.

### Architecture

The project follows a modular, agent-based architecture:

*   **Agent Kernel (`src/codex/kernel.py`):** The central component of the Python application. It's responsible for orchestrating command processing, routing commands to the appropriate agents, and managing the application's state.
*   **Agents:** The project includes several agents with distinct roles, such as the "Artemis" governance agent, the "Copilot" assistant agent, and the "Pack Rat" data transfer agent.
*   **Artemis Transmission Protocol (ATP):** A structured communication protocol that enables agents to exchange messages with clear intent and context.
*   **Memory Layer:** A Node.js/TypeScript application that provides a REST API for interacting with an Obsidian vault. This allows agents to store and retrieve information, effectively giving them a persistent memory.
*   **Trust Interface:** A system for managing trust scores for agents, which are used to control access to the memory layer.

## Building and Running

### 1. Set up the Environment

1.  **Install Python dependencies:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```
2.  **Install Node.js dependencies for the Memory Layer:**
    ```bash
    cd "src/Artemis Agentic Memory Layer"
    npm install
    cd ../..
    ```
3.  **Set up environment variables:**
    *   Copy `.env.example` to `.env` and fill in the required values, including API keys for the MCP server and Obsidian.

### 2. Run the Application

1.  **Start the MCP Memory Server:**
    ```bash
    cd "src/Artemis Agentic Memory Layer"
    npm run dev
    ```
2.  **Run the CLI (in another terminal):**
    ```bash
    source .venv/bin/activate
    python src/codex/codex_cli.py
    ```

### 3. Run the tests

*   **Run all python tests:**
    ```bash
    pytest
    ```
*   **Run python tests with coverage:**
    ```bash
    pytest --cov=src
    ```

## Development Conventions

*   **Coding Style:** The project follows the PEP 8 style guide for Python code and uses `black`, `isort`, and `flake8` to enforce it.
*   **Testing:** The project has a strong emphasis on testing. All new features should be accompanied by unit and/or integration tests.
*   **Documentation:** The `docs` directory contains a wealth of information about the project's architecture, features, and APIs. All new features should be documented.
*   **Commit Messages:** Follow the conventional commit format.
*   **Branching:** Use feature branches for all new work.
*   **Pull Requests:** All pull requests must be reviewed and approved before being merged.
*   **Security:** The project has a strong focus on security. All secrets should be stored in environment variables and never committed to the repository.

This guide should provide a solid foundation for any AI assistant working on the Artemis-City project. For more detailed information, please refer to the documents in the `docs` directory.
