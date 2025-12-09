# Obsidian Model Context Protocol (MCP) Server

This project implements a Model Context Protocol (MCP) server designed to act as a lightweight REST-based interface between your agentic frameworks (LLM agents) and an Obsidian knowledge store. It allows your agents to programmatically interact with your Obsidian vault, treating it as a dynamic memory bus.

## Table of Contents

- [What is the MCP Server?](#what-is-the-mcp-server)
- [Prerequisites](#prerequisites)
- [Setup & Installation](#setup--installation)
  - [1. Clone the repository](#1-clone-the-repository)
  - [2. Install dependencies](#2-install-dependencies)
  - [3. Configure Environment Variables](#3-configure-environment-variables)
- [Running the Application](#running-the-application)
  - [1. Locally (Development Mode)](#1-locally-development-mode)
  - [2. Locally (Production Build)](#2-locally-production-build)
  - [3. Using Docker (Recommended for Agentic Workflows)](#3-using-docker-recommended-for-agentic-workflows)
- [API Endpoints](#api-endpoints)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)
- [License](#license)

## What is the MCP Server?

The MCP server provides a set of HTTP endpoints (e.g., `/getContext`, `/appendContext`, `/searchNotes`) that translate agent requests into vault reads and writes. This decouples your agents from the underlying knowledge store, enabling robust multi-agent workflows where agents can fetch, update, and coordinate around a single, versioned source of truth – your Obsidian vault.

## Prerequisites

Before you begin, ensure you have the following installed and configured:

1. **Node.js (v18 or higher)**: You can download it from [nodejs.org](https://nodejs.org/).
2. **npm** (Node Package Manager): Usually comes bundled with Node.js.
3. **Obsidian**: The note-taking application. Download it from [obsidian.md](https://obsidian.md/). Ensure your vault is open and accessible when the MCP server attempts to connect.
4. **Obsidian Local REST API Plugin**: Install this plugin within your Obsidian vault. Go to `Settings` -> `Community Plugins` -> `Browse` and search for "Local REST API". Install and **enable** it.
5. **Obsidian API Key**: After enabling the Local REST API plugin, go to its settings. You will find an option to generate an API key. **Copy this key**, as it will be needed for the `OBSIDIAN_API_KEY` environment variable.
6. **Obsidian Local REST API Port**: Note the port where the Obsidian Local REST API listens (default is `27124`). This will be part of `OBSIDIAN_BASE_URL`.

## Setup & Installation

Follow these steps to get the MCP server up and running:

### 1. Clone the repository

```bash
git clone <repository-url>
cd obsidian-mcp-server
```

If you received these files directly, navigate into the `obsidian-mcp-server` directory.

### 2. Install dependencies

```bash
npm install
```

### 3. Configure Environment Variables

Create a `.env` file in the root of the `obsidian-mcp-server` directory. You can copy the provided `.env.example`:

```bash
cp .env.example .env
```

Open the newly created `.env` file and update the following variables with your specific values:

- `MCP_API_KEY`: A secret key for your agents to authenticate with _this_ MCP server. **Choose a strong, unique key.** This protects your MCP server from unauthorized access.
- `OBSIDIAN_BASE_URL`: The URL where your Obsidian Local REST API is listening.
  - **If running MCP server directly on your machine (not Docker):** `https://127.0.0.1:27124` (replace `27124` if your Obsidian uses a different port).
  - **If running MCP server in Docker (Obsidian on host - Mac/Windows):** `https://host.docker.internal:27124` (replace `27124` if needed). This special Docker DNS name resolves to your host machine.
  - **If running MCP server in Docker (Obsidian on host - Linux):** You might need to find your host machine's IP address (e.g., `ip addr show docker0` to find the bridge IP, often `172.17.0.1`) or use `network_mode: host` in `docker-compose.yml` (which exposes all host ports). A common approach is `https://<HOST_IP_ADDRESS>:27124`.
- `OBSIDIAN_API_KEY`: The API key you generated from the Obsidian Local REST API plugin settings.

Your `.env` file should look something like this (with your actual keys):

```ini
PORT=3000
MCP_API_KEY=your_super_secret_mcp_key_123_CHANGE_ME
OBSIDIAN_BASE_URL=https://127.0.0.1:27124
OBSIDIAN_API_KEY=your_obsidian_plugin_api_key_xyz_CHANGE_ME
MCP_LOG_LEVEL=info
```

## Running the Application

You have two primary ways to run the MCP server:

### 1. Locally (Development Mode)

This is ideal for development as it provides hot-reloading.

```bash
npm run dev
```

The server will start on `http://localhost:3000` (or the `PORT` you configured).

### 2. Locally (Production Build)

First, build the TypeScript project:

```bash
npm run build
```

Then, start the compiled JavaScript application:

```bash
npm start
```

### 3. Using Docker (Recommended for Agentic Workflows)

Ensure Docker Desktop is running on your machine.

1. **Build and run the Docker container:**

    ```bash
    docker-compose up --build
    ```

    This command will build the Docker image (if it doesn't exist or has changed) and start the MCP server in a container.

2. **Verify:**
    The server will be accessible on `http://localhost:3000` from your host machine. Remember to set `OBSIDIAN_BASE_URL` in your `.env` (or `docker-compose.yml` environment section) to `https://host.docker.internal:27124` if Obsidian is running on your host machine (Mac/Windows). For Linux hosts, refer to the `OBSIDIAN_BASE_URL` explanation in the [Configure Environment Variables](#3-configure-environment-variables) section.

## API Endpoints

Once the server is running, you can interact with it using HTTP requests. All requests should include an `Authorization` header with your `MCP_API_KEY` (e.g., `Authorization: Bearer your_super_secret_mcp_key_123`).

**Base URL for all endpoints:** `http://localhost:3000/api` (or your configured `PORT`)

---

- `POST /getContext`
  - **Description:** Reads the content of a specific note.
  - **Request Body:**

    ```json
    { "path": "path/to/your/Note.md" }
    ```

  - **Example (curl):**

    ```bash
    curl -X POST http://localhost:3000/api/getContext \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer your_super_secret_mcp_key_123_CHANGE_ME" \
      -d '{ "path": "My Daily Notes/2023-10-27.md" }'
    ```

  - **Success Response (200 OK):**

    ```json
    {
      "success": true,
      "data": {
        "path": "My Daily Notes/2023-10-27.md",
        "content": "# Daily Notes\n\n- Task 1\n- Task 2"
      }
    }
    ```

  - **Error Response (400 Bad Request / 500 Internal Server Error):**

    ```json
    { "success": false, "error": "Missing note path." }
    ```

    ```json
    { "success": false, "error": "Error reading note '...' : ..." }
    ```

---

- `POST /appendContext`
  - **Description:** Appends content to an existing note or creates a new one if it doesn't exist.
  - **Request Body:**

    ```json
    { "path": "path/to/your/Note.md", "content": "New content to append." }
    ```

  - **Example (curl):**

    ```bash
    curl -X POST http://localhost:3000/api/appendContext \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer your_super_secret_mcp_key_123_CHANGE_ME" \
      -d '{ "path": "My Daily Notes/2023-10-27.md", "content": "\n- New item added by agent." }'
    ```

  - **Success Response (200 OK):**

    ```json
    {
      "success": true,
      "message": "Content appended to note 'My Daily Notes/2023-10-27.md'."
    }
    ```

---

- `POST /updateNote`
  - **Description:** Overwrites the entire content of a note. If the note does not exist, it will be created.
  - **Request Body:**

    ```json
    { "path": "path/to/your/Note.md", "content": "New full content." }
    ```

  - **Example (curl):**

    ```bash
    curl -X POST http://localhost:3000/api/updateNote \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer your_super_secret_mcp_key_123_CHANGE_ME" \
      -d '{ "path": "My Project/Status.md", "content": "# Project Status\n\nUpdated: 2023-10-27\n\nAll tasks are green." }'
    ```

  - **Success Response (200 OK):**

    ```json
    { "success": true, "message": "Note 'My Project/Status.md' updated." }
    ```

---

- `POST /searchNotes`
  - **Description:** Searches for notes within the vault based on a query.
  - **Request Body:**

    ```json
    { "query": "search term" }
    ```

  - **Example (curl):**

    ```bash
    curl -X POST http://localhost:3000/api/searchNotes \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer your_super_secret_mcp_key_123_CHANGE_ME" \
      -d '{ "query": "project status" }'
    ```

  - **Success Response (200 OK):**

    ```json
    {
      "success": true,
      "data": [
        {
          "path": "My Project/Status.md",
          "excerpt": "Project Status Updated: 2023-10-27..."
        },
        {
          "path": "Meeting Notes/Project Alpha.md",
          "excerpt": "Discussed current project status..."
        }
      ]
    }
    ```

---

- `POST /listNotes`
  - **Description:** Lists all notes (paths) in the vault.
  - **Request Body:** `{}` (empty object)
  - **Example (curl):**

    ```bash
    curl -X POST http://localhost:3000/api/listNotes \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer your_super_secret_mcp_key_123_CHANGE_ME" \
      -d '{}'
    ```

  - **Success Response (200 OK):**

    ```json
    {
      "success": true,
      "data": [
        "My Daily Notes/2023-10-27.md",
        "My Project/Status.md",
        "Meeting Notes/Project Alpha.md",
        "Inbox/New Idea.md"
      ]
    }
    ```

---

- `POST /deleteNote`
  - **Description:** Deletes a note from the vault.
  - **Request Body:**

    ```json
    { "path": "path/to/note/to/delete.md" }
    ```

  - **Example (curl):**

    ```bash
    curl -X POST http://localhost:3000/api/deleteNote \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer your_super_secret_mcp_key_123_CHANGE_ME" \
      -d '{ "path": "Inbox/Old Idea.md" }'
    ```

  - **Success Response (200 OK):**

    ```json
    {
      "success": true,
      "message": "Note 'Inbox/Old Idea.md' deleted successfully."
    }
    ```

---

- `POST /manageFrontmatter`
  - **Description:** Updates a frontmatter key-value pair in a note. If the key does not exist, it will be added. If the note does not have frontmatter, it will be added.
  - **Request Body:**

    ```json
    { "path": "path/to/note.md", "key": "status", "value": "completed" }
    ```

  - **Example (curl):**

    ```bash
    curl -X POST http://localhost:3000/api/manageFrontmatter \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer your_super_secret_mcp_key_123_CHANGE_ME" \
      -d '{ "path": "My Project/Task A.md", "key": "status", "value": "completed" }'
    ```

  - **Success Response (200 OK):**

    ```json
    {
      "success": true,
      "message": "Frontmatter for 'My Project/Task A.md' updated."
    }
    ```

---

- `POST /manageTags`
  - **Description:** Adds or removes tags from a note's frontmatter.
  - **Request Body (Add Tags):**

    ```json
    { "path": "path/to/note.md", "tags": ["tag1", "tag2"], "action": "add" }
    ```

  - **Request Body (Remove Tags):**

    ```json
    { "path": "path/to/note.md", "tags": ["tag1"], "action": "remove" }
    ```

  - **Example (curl - Add):**

    ```bash
    curl -X POST http://localhost:3000/api/manageTags \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer your_super_secret_mcp_key_123_CHANGE_ME" \
      -d '{ "path": "My Project/Task A.md", "tags": ["urgent", "review"], "action": "add" }'
    ```

  - **Example (curl - Remove):**

    ```bash
    curl -X POST http://localhost:3000/api/manageTags \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer your_super_secret_mcp_key_123_CHANGE_ME" \
      -d '{ "path": "My Project/Task A.md", "tags": ["review"], "action": "remove" }'
    ```

  - **Success Response (200 OK):**

    ```json
    {
      "success": true,
      "message": "Tags for 'My Project/Task A.md' added successfully."
    }
    ```

---

- `POST /searchReplace`
  - **Description:** Performs a search and replace operation within the content of a specific note.
  - **Request Body:**

    ```json
    {
      "path": "path/to/note.md",
      "search": "old string",
      "replace": "new string"
    }
    ```

  - **Example (curl):**

    ```bash
    curl -X POST http://localhost:3000/api/searchReplace \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer your_super_secret_mcp_key_123_CHANGE_ME" \
      -d '{ "path": "My Project/Report.md", "search": "draft", "replace": "final" }'
    ```

  - **Success Response (200 OK):**

    ```json
    {
      "success": true,
      "data": {
        "path": "My Project/Report.md",
        "content": "Updated content after replacement."
      },
      "message": "Search and replace in 'My Project/Report.md' successful."
    }
    ```

---

## Security Considerations

- **API Keys:** Both `MCP_API_KEY` and `OBSIDIAN_API_KEY` grant significant access.
  - **`MCP_API_KEY`**: This key protects your MCP server. Anyone with this key can read, write, and delete notes in your Obsidian vault via the MCP server. Keep it secret and secure.
  - **`OBSIDIAN_API_KEY`**: This key grants direct access to your Obsidian vault via the Local REST API plugin. It should be treated with extreme care.
- **HTTPS:** The Obsidian Local REST API uses HTTPS. The MCP server is configured to `rejectUnauthorized: false` for the `httpsAgent` to allow self-signed certificates, which is common for local development. For production deployments or if exposing the MCP server publicly, ensure proper certificate validation is in place or use a reverse proxy that handles SSL termination.
- **Network Exposure:** By default, the MCP server runs on `localhost:3000`. If you expose it to a wider network, ensure it's behind a firewall and only accessible by trusted agents/systems.
- **Input Validation:** While the MCP server performs basic input validation (e.g., checking for `path` and `content`), malicious input could potentially lead to unexpected behavior in Obsidian. Always sanitize or validate agent inputs before sending them to the MCP server.

## Troubleshooting

- **`MCP_API_KEY is not set` or `OBSIDIAN_BASE_URL is not set` errors:**
  - Ensure you have created a `.env` file in the root directory.
  - Verify that all required environment variables (`MCP_API_KEY`, `OBSIDIAN_BASE_URL`, `OBSIDIAN_API_KEY`) are present and correctly populated in your `.env` file.
  - If running in Docker, check the `environment` section of your `docker-compose.yml` file.
- **`Error: connect ECONNREFUSED` or similar network errors:**
  - **Obsidian Local REST API not running:** Make sure Obsidian is open and the "Local REST API" plugin is enabled and running.
  - **Incorrect `OBSIDIAN_BASE_URL`:** Double-check the port (default `27124`) and IP address in your `OBSIDIAN_BASE_URL`.
  - **Firewall:** Your firewall might be blocking the connection between the MCP server and Obsidian.
  - **Docker network issues (Linux hosts):** If running MCP in Docker on Linux, `host.docker.internal` won't work. Use your host machine's actual IP address (e.g., `172.17.0.1` or your LAN IP if Obsidian is exposed) for `OBSIDIAN_BASE_URL`.
- **`Forbidden: Invalid API Key.` (403 error from MCP server):**
  - The `Authorization` header in your agent's request does not match the `MCP_API_KEY` set in your `.env` file.
  - Ensure the header is `Authorization: Bearer your_mcp_secret_key`.
- **`Unauthorized` or `Forbidden` errors from Obsidian (via MCP server):**
  - The `OBSIDIAN_API_KEY` configured in your `.env` file is incorrect or has expired. Generate a new one in Obsidian's plugin settings and update your `.env`.
- **Note not found / Operation failed:**
  - Verify the `path` provided in your request body is correct and matches the exact path within your Obsidian vault (including file extension, e.g., `.md`).
  - Ensure the note actually exists if you're trying to read, update, or delete an existing note.

## Next Steps

Integrate this MCP server into your agentic frameworks by making HTTP requests to its endpoints. Ensure your agents pass the `MCP_API_KEY` for authentication. Happy agent building!

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
