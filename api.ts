/**
 * API Client for MCP Dashboard
 *
 * Provides functions to interact with the MCP backend API.
 * All endpoints are proxied through Vite dev server during development.
 *
 * @module api
 */

/** Base URL for API endpoints (proxied by Vite in development) */
const API_BASE_URL = '/api';

/**
 * Fetch all registered agents from the MCP server.
 *
 * @returns Promise resolving to an array of agent objects
 * @throws Error if the request fails
 */
export const fetchAgents = async () => {
  const response = await fetch(`${API_BASE_URL}/agents`);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
};

/**
 * Fetch all tasks from the Obsidian vault.
 *
 * @returns Promise resolving to an array of task objects
 * @throws Error if the request fails
 */
export const fetchTasks = async () => {
  const response = await fetch(`${API_BASE_URL}/tasks`);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
};

/**
 * Create a new task in the Obsidian vault.
 *
 * @param taskData - Task data including agent, title, context, and keywords
 * @returns Promise resolving to the created task object
 * @throws Error if the request fails
 */
export const createNewTask = async (taskData: any) => {
  const response = await fetch(`${API_BASE_URL}/tasks`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(taskData),
  });
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
};

/**
 * Fetch all available reports from the MCP server.
 *
 * @returns Promise resolving to an array of report summary objects
 * @throws Error if the request fails
 */
export const fetchReports = async () => {
  const response = await fetch(`${API_BASE_URL}/reports`);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
};

/**
 * Fetch the content of a specific report.
 *
 * @param filename - Name of the report file to fetch
 * @returns Promise resolving to the report content object
 * @throws Error if the request fails
 */
export const fetchReportContent = async (filename: string) => {
  const response = await fetch(`${API_BASE_URL}/reports/${filename}`);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
};

/**
 * Execute a single pending task by its relative path.
 *
 * @param relativePath - Path to the task file in the Obsidian vault
 * @returns Promise resolving to the execution result
 * @throws Error if the request fails
 */
export const executePendingTask = async (relativePath: string) => {
  const response = await fetch(`${API_BASE_URL}/execute-task`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ relative_path: relativePath }),
  });
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
};

/**
 * Execute all pending tasks in batch.
 *
 * @returns Promise resolving to a summary with completed, failed, and skipped counts
 * @throws Error if the request fails
 */
export const executeAllPendingTasks = async () => {
  const response = await fetch(`${API_BASE_URL}/execute-all-pending`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  });
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
};

/**
 * Fetch all agent scores with performance metrics.
 *
 * @returns Promise resolving to an array of agent score objects
 * @throws Error if the request fails
 */
export const fetchAgentScores = async () => {
  const response = await fetch(`${API_BASE_URL}/db/agents`);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
};

/**
 * Fetch Hebbian network statistics.
 *
 * @returns Promise resolving to network stats (connections, weights, activation counts)
 * @throws Error if the request fails
 */
export const fetchHebbianStats = async () => {
  const response = await fetch(`${API_BASE_URL}/db/hebbian/stats`);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
};

/**
 * Fetch top Hebbian network connections.
 *
 * @param limit - Maximum number of connections to return (default: 50)
 * @returns Promise resolving to an array of connection objects
 * @throws Error if the request fails
 */
export const fetchHebbianConnections = async (limit: number = 50) => {
  const response = await fetch(
    `${API_BASE_URL}/db/hebbian/connections?limit=${limit}`
  );
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
};

/**
 * Fetch Hebbian statistics for a specific agent.
 *
 * @param agentName - Name of the agent to query
 * @returns Promise resolving to agent-specific Hebbian stats
 * @throws Error if the request fails
 */
export const fetchAgentHebbianStats = async (agentName: string) => {
  const response = await fetch(
    `${API_BASE_URL}/db/hebbian/agent/${encodeURIComponent(agentName)}`
  );
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
};

/**
 * Fetch vector store statistics.
 *
 * @returns Promise resolving to vector stats (total docs, avg length)
 * @throws Error if the request fails
 */
export const fetchVectorStats = async () => {
  const response = await fetch(`${API_BASE_URL}/db/vectors/stats`);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
};

/**
 * Fetch paginated vectors from the vector store.
 *
 * @param limit - Maximum number of vectors to return (default: 100)
 * @param offset - Number of vectors to skip (default: 0)
 * @returns Promise resolving to an array of vector objects
 * @throws Error if the request fails
 */
export const fetchVectors = async (limit: number = 100, offset: number = 0) => {
  const response = await fetch(
    `${API_BASE_URL}/db/vectors/list?limit=${limit}&offset=${offset}`
  );
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
};

/**
 * Fetch recent run summaries from the run logs.
 *
 * @param limit - Maximum number of runs to return (default: 20)
 * @returns Promise resolving to an array of run summary objects
 * @throws Error if the request fails
 */
export const fetchRuns = async (limit: number = 20) => {
  const response = await fetch(`${API_BASE_URL}/db/runs?limit=${limit}`);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
};

/**
 * Fetch events for a specific run.
 *
 * @param runId - ID of the run to query
 * @param eventType - Optional event type filter
 * @returns Promise resolving to an array of event objects
 * @throws Error if the request fails
 */
export const fetchRunEvents = async (
  runId: string,
  eventType?: string
) => {
  const url = new URL(`${window.location.origin}${API_BASE_URL}/db/runs/${encodeURIComponent(runId)}/events`);
  if (eventType) {
    url.searchParams.append('event_type', eventType);
  }
  const response = await fetch(url.toString());
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
};

/**
 * Execute a CLI-style instruction through the executor.
 *
 * @param data - Execution request data (instruction, optional agent, capability, title)
 * @returns Promise resolving to execution result (task_id, status, summary, note_path, error)
 * @throws Error if the request fails
 */
export const executeInstruction = async (data: {
  instruction: string;
  capability?: string;
  agent?: string;
  title?: string;
}) => {
  const response = await fetch(`${API_BASE_URL}/cli/execute`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
};
