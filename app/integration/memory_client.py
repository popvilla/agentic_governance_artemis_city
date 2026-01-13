"""Memory client for Artemis Agentic Memory Layer (MCP Server).

This module provides a Python REST client for interacting with the
Obsidian MCP server, enabling agents to read/write to the knowledge vault.
"""

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional


class MCPOperation(Enum):
    """MCP server operation types."""

    GET_CONTEXT = "getContext"
    APPEND_CONTEXT = "appendContext"
    UPDATE_NOTE = "updateNote"
    SEARCH_NOTES = "searchNotes"
    LIST_NOTES = "listNotes"
    DELETE_NOTE = "deleteNote"
    MANAGE_FRONTMATTER = "manageFrontmatter"
    MANAGE_TAGS = "manageTags"
    SEARCH_REPLACE = "searchReplace"


@dataclass
class MCPResponse:
    """Standardized MCP server response.

    Attributes:
        success: Whether operation succeeded
        data: Response data (if successful)
        message: Success message (optional)
        error: Error message (if failed)
        status_code: HTTP status code
    """

    success: bool
    data: Optional[Any] = None
    message: Optional[str] = None
    error: Optional[str] = None
    status_code: int = 200

    @classmethod
    def from_json(cls, json_data: Dict, status_code: int) -> 'MCPResponse':
        """Create MCPResponse from JSON data.

        Args:
            json_data: JSON response from server
            status_code: HTTP status code

        Returns:
            MCPResponse instance
        """
        return cls(
            success=json_data.get('success', False),
            data=json_data.get('data'),
            message=json_data.get('message'),
            error=json_data.get('error'),
            status_code=status_code,
        )


class MemoryClient:
    """Client for Artemis Agentic Memory Layer (MCP Server).

    Provides methods to interact with Obsidian vault via REST API,
    following the standardized MCP response format.

    Attributes:
        base_url: Base URL of MCP server
        api_key: Bearer token for authentication
        timeout: Request timeout in seconds
    """

    DEFAULT_TIMEOUT = 30  # seconds

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        """Initialize memory client.

        Args:
            base_url: MCP server base URL (defaults to env MCP_BASE_URL)
            api_key: MCP API key (defaults to env MCP_API_KEY)
            timeout: Request timeout in seconds
        """
        self.base_url = (
            base_url if base_url is not None else os.getenv('MCP_BASE_URL', 'http://localhost:3000')
        )
        self.api_key = api_key if api_key is not None else os.getenv('MCP_API_KEY', '')
        self.timeout = timeout

        # Ensure base_url doesn't end with slash
        self.base_url = self.base_url.rstrip('/')

        if not self.api_key:
            raise ValueError("MCP_API_KEY required. Set via environment variable or constructor.")

    def _make_request(self, operation: MCPOperation, data: Optional[Dict] = None) -> MCPResponse:
        """Make HTTP request to MCP server.

        Args:
            operation: MCP operation to perform
            data: Request body data

        Returns:
            MCPResponse with result

        Raises:
            urllib.error.URLError: If request fails
        """
        url = f"{self.base_url}/api/{operation.value}"

        # Prepare request
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.api_key}'}

        request_data = json.dumps(data or {}).encode('utf-8')
        req = urllib.request.Request(url, data=request_data, headers=headers, method='POST')

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                response_data = json.loads(response.read().decode('utf-8'))
                return MCPResponse.from_json(response_data, response.status)

        except urllib.error.HTTPError as e:
            # Parse error response
            try:
                error_data = json.loads(e.read().decode('utf-8'))
                return MCPResponse.from_json(error_data, e.code)
            except (json.JSONDecodeError, AttributeError):
                return MCPResponse(
                    success=False, error=f"HTTP {e.code}: {e.reason}", status_code=e.code
                )

        except urllib.error.URLError as e:
            return MCPResponse(
                success=False, error=f"Connection error: {str(e.reason)}", status_code=0
            )
        except Exception as e:
            return MCPResponse(success=False, error=f"Unexpected error: {str(e)}", status_code=0)

    def get_context(self, path: str) -> MCPResponse:
        """Read content of a note.

        Args:
            path: Path to note in vault (e.g., "Daily/2025-11-23.md")

        Returns:
            MCPResponse with note content in data field
        """
        return self._make_request(MCPOperation.GET_CONTEXT, {'path': path})

    def append_context(self, path: str, content: str) -> MCPResponse:
        """Append content to a note (creates if doesn't exist).

        Args:
            path: Path to note in vault
            content: Content to append

        Returns:
            MCPResponse with success status
        """
        return self._make_request(MCPOperation.APPEND_CONTEXT, {'path': path, 'content': content})

    def update_note(self, path: str, content: str) -> MCPResponse:
        """Replace entire note content.

        Args:
            path: Path to note in vault
            content: New content (replaces existing)

        Returns:
            MCPResponse with success status
        """
        return self._make_request(MCPOperation.UPDATE_NOTE, {'path': path, 'content': content})

    def search_notes(self, query: str, context_length: int = 100) -> MCPResponse:
        """Search notes for query string.

        Args:
            query: Search query
            context_length: Characters of context around matches

        Returns:
            MCPResponse with search results
        """
        return self._make_request(
            MCPOperation.SEARCH_NOTES, {'query': query, 'contextLength': context_length}
        )

    def list_notes(self, folder: str = "") -> MCPResponse:
        """List all notes in vault or specific folder.

        Args:
            folder: Optional folder path to list

        Returns:
            MCPResponse with list of note paths
        """
        data = {'folder': folder} if folder else {}
        return self._make_request(MCPOperation.LIST_NOTES, data)

    def delete_note(self, path: str) -> MCPResponse:
        """Delete a note from vault.

        Args:
            path: Path to note to delete

        Returns:
            MCPResponse with success status
        """
        return self._make_request(MCPOperation.DELETE_NOTE, {'path': path})

    def manage_frontmatter(
        self, path: str, action: str, key: Optional[str] = None, value: Optional[str] = None
    ) -> MCPResponse:
        """Manage YAML frontmatter in note.

        Args:
            path: Path to note
            action: Action to perform (get, set, delete, list)
            key: Frontmatter key (for set/delete)
            value: Frontmatter value (for set)

        Returns:
            MCPResponse with frontmatter data or success status
        """
        data = {'path': path, 'action': action}
        if key:
            data['key'] = key
        if value:
            data['value'] = value

        return self._make_request(MCPOperation.MANAGE_FRONTMATTER, data)

    def manage_tags(self, path: str, action: str, tags: Optional[List[str]] = None) -> MCPResponse:
        """Manage tags in note.

        Args:
            path: Path to note
            action: Action to perform (get, add, remove, set)
            tags: List of tags (for add/remove/set actions)

        Returns:
            MCPResponse with tag data or success status
        """
        data = {'path': path, 'action': action}
        if tags:
            data['tags'] = tags

        return self._make_request(MCPOperation.MANAGE_TAGS, data)

    def search_replace(
        self, path: str, search: str, replace: str, regex: bool = False
    ) -> MCPResponse:
        """Search and replace text in note.

        Args:
            path: Path to note
            search: Text/pattern to search for
            replace: Replacement text
            regex: Whether to use regex matching

        Returns:
            MCPResponse with number of replacements made
        """
        return self._make_request(
            MCPOperation.SEARCH_REPLACE,
            {'path': path, 'search': search, 'replace': replace, 'regex': regex},
        )

    def health_check(self) -> bool:
        """Check if MCP server is accessible.

        Returns:
            True if server is healthy, False otherwise
        """
        try:
            url = f"{self.base_url}/health"
            req = urllib.request.Request(url, method='GET')

            with urllib.request.urlopen(req, timeout=5) as response:
                return response.status == 200
        except Exception:
            # Catch all exceptions during health check (network, timeout, etc.)
            return False

    def get_agent_context(self, agent_name: str, limit: int = 10) -> MCPResponse:
        """Get recent context for a specific agent.

        This is a convenience method that searches for notes
        tagged with the agent name.

        Args:
            agent_name: Name of agent to get context for
            limit: Maximum number of notes to return

        Returns:
            MCPResponse with agent context notes
        """
        # Search for notes tagged with agent
        tag_query = f"#{agent_name}"
        response = self.search_notes(tag_query)

        if response.success and response.data:
            # Limit results
            results = response.data.get('results', [])[:limit]
            return MCPResponse(
                success=True,
                data={'results': results},
                message=f"Found {len(results)} context notes for {agent_name}",
            )

        return response

    def store_agent_context(
        self, agent_name: str, context: str, folder: str = "Agents/Context"
    ) -> MCPResponse:
        """Store context for an agent in the vault.

        Creates or appends to an agent-specific context file.

        Args:
            agent_name: Name of agent
            context: Context to store
            folder: Folder to store context in

        Returns:
            MCPResponse with success status
        """
        from datetime import datetime

        # Create timestamped entry
        timestamp = datetime.now().isoformat()
        entry = f"\n\n## {timestamp}\n\n{context}\n"

        # Append to agent's context file
        path = f"{folder}/{agent_name}_context.md"
        response = self.append_context(path, entry)

        if response.success:
            # Add agent tag
            self.manage_tags(path, 'add', [agent_name, 'agent-context'])

        return response
