# Artemis City

## Overview

Artemis City is an architectural framework designed to align agentic reasoning with transparent, accountable action across distributed intelligence systems—both human and machine. This initial scaffolding, Version Zero, provides a foundational structure for defining agents, managing memory, establishing interfaces, and simulating environments. The project is seeded with the intention of iterative clarity and accountable collaboration, balancing trust, entropy, and collaboration to move towards a "net good over noise" ethos.

This repository contains a command-line interface (CLI) to interact with the system's agent router, along with a standalone simulation for mail delivery within the "Sandbox City" environment.

## Prerequisites

Before you begin, ensure you have the following software installed on your system:
- **Python 3.8 or higher**: The core CLI and simulation scripts are written in Python.
- **pip**: Python's package installer, which typically comes with Python.

## Setup and Installation

Follow these steps to get Artemis City running on your local machine:

1.  **Clone the Repository**:
    If this were a Git repository, you would clone it. For now, ensure all project files are located in a single directory.

2.  **Navigate to the Project Directory**:
    Open your terminal and change to the directory containing the project files.

3.  **Create and Activate a Virtual Environment**:
    It is highly recommended to use a virtual environment to manage dependencies.

    ```bash
    # Create the virtual environment
    python -m venv venv

    # Activate on macOS and Linux
    source venv/bin/activate

    # Activate on Windows
    .\venv\Scripts\activate
    ```

4.  **Install Dependencies**:
    Install the required Python packages using the `requirements.txt` file.

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Artemis City can be operated through its command-line interface or by running individual simulations.

### Running the Agentic Codex CLI

The main entry point is the Agentic Codex CLI, which simulates routing commands to different agents based on keywords.

1.  **Launch the CLI in Interactive Mode**:
    Run the `codex_cli.py` script without any arguments to enter an interactive session.

    ```bash
    python interface/codex_cli.py
    ```

    You will be greeted with a `codex>` prompt. Type commands and press Enter to see how they are routed. To exit, type `exit` or `quit`.

    **Example Session**:
    ```
    --- Agentic Codex CLI ---
    Type 'exit' or 'quit' to close.
    codex> ask artemis about system status
    CLI received command: 'ask artemis about system status'
    Routing command to Artemis (Overseer of the city's functions):
      - Input: 'ask artemis about system status'
      - Expected action: processing system-level commands and queries...
    codex> help me with a data query
    CLI received command: 'help me with a data query'
    Routing command to Copilot (Data retrieval and analysis assistant):
      - Input: 'help me with a data query'
      - Expected action: assisting with data-related tasks...
    ```

2.  **Run the CLI with a Command**:
    You can also pass a command directly as an argument. The script will execute it and then exit.

    ```bash
    python interface/codex_cli.py "check mail for delivery"
    ```

    **Example Output**:
    ```
    --- Agentic Codex CLI ---
    Type 'exit' or 'quit' to close.
    CLI received command: 'check mail for delivery'
    Routing command to Pack Rat (Secure data courier):
      - Input: 'check mail for delivery'
      - Expected action: handling secure data transfer and storage...
    ```

### Running the Mail Delivery Simulation

The `mail_delivery_sim.py` script simulates a secure mail delivery process within the Sandbox City environment.

-   **Execute the script directly from your terminal**:

    ```bash
    python sandbox_city/networked_scripts/mail_delivery_sim.py
    ```

    The script will run two predefined simulations and print the results, including a simulated delay and a random chance of failure.

    **Example Output**:
    ```
    Running Mail Delivery Simulation (Sandbox City - Post Office)

    --- Mail Delivery Simulation ---
    Sender: Agent_A, Recipient: Agent_B
    Message: 'Urgent operational update.'
    Pack Rat is initiating secure transfer...
    Transfer successful: Message delivered securely.

    --- Mail Delivery Simulation ---
    Sender: Human_User, Recipient: Artemis
    Message: 'Query about recent policy change.'
    Pack Rat is initiating secure transfer...
    Transfer failed: Data integrity compromised or recipient unreachable.
    ```