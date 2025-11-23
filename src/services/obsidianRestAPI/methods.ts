import { obsidianAPI } from './index';

interface ObsidianNote {
  path: string;
  content: string;
  // Add other potential properties from Obsidian API like frontmatter, tags, etc.
}

interface SearchResult {
  path: string;
  excerpt: string;
  // Add other potential properties
}

/**
 * Reads the content of a specific note from Obsidian.
 * @param path The path to the note (e.g., 'My Folder/My Note.md').
 * @returns The content of the note.
 */
export async function readNote(path: string): Promise<string> {
  const response = await obsidianAPI.get<ObsidianNote>(`/vault/read`, {
    params: { path },
  });
  return response.data.content;
}

/**
 * Updates an existing note or creates a new one. Can append content.
 * @param path The path to the note.
 * @param content The new content for the note.
 * @param options Options, e.g., { append: true } to append content.
 * @returns A success message.
 */
export async function updateNote(path: string, content: string, options?: { append?: boolean }): Promise<string> {
  const response = await obsidianAPI.post(`/vault/write`, {
    path,
    content,
    cursor: options?.append ? { line: -1, ch: -1 } : undefined, // Append to end if 'append' is true
  });
  return response.data.message || 'Note updated successfully.';
}

/**
 * Searches for notes within the Obsidian vault.
 * @param query The search query string.
 * @returns An array of search results.
 */
export async function searchNotes(query: string): Promise<SearchResult[]> {
  const response = await obsidianAPI.get<SearchResult[]>(`/vault/search`, {
    params: { query },
  });
  return response.data;
}

/**
 * Lists all notes in the Obsidian vault.
 * @returns An array of note paths.
 */
export async function listNotes(): Promise<string[]> {
  const response = await obsidianAPI.get<{ files: string[] }>(`/vault/list`);
  return response.data.files;
}

/**
 * Deletes a note from the Obsidian vault.
 * @param path The path to the note to delete.
 * @returns A success message.
 */
export async function deleteNote(path: string): Promise<string> {
  const response = await obsidianAPI.delete(`/vault/delete`, {
    params: { path },
  });
  return response.data.message || 'Note deleted successfully.';
}

/**
 * Manages frontmatter for a note.
 * Note: The Obsidian Local REST API might not have a direct endpoint for this.
 * This implementation assumes a hypothetical `/vault/frontmatter` endpoint.
 * If not available, this would require reading the note, parsing/modifying content, and writing back.
 * @param path The path to the note.
 * @param key The frontmatter key.
 * @param value The value to set for the key.
 * @returns A success message.
 */
export async function manageFrontmatter(path: string, key: string, value: any): Promise<string> {
  const response = await obsidianAPI.post(`/vault/frontmatter`, {
    path,
    key,
    value,
  });
  return response.data.message || 'Frontmatter updated successfully.';
}

/**
 * Manages tags for a note (add or remove).
 * Note: The Obsidian Local REST API might not have a direct endpoint for this.
 * This implementation assumes a hypothetical `/vault/tags` endpoint.
 * If not available, this would require reading the note, parsing/modifying content, and writing back.
 * @param path The path to the note.
 * @param tags An array of tags to add or remove.
 * @param action 'add' or 'remove'.
 * @returns A success message.
 */
export async function manageTags(path: string, tags: string[], action: 'add' | 'remove'): Promise<string> {
  const response = await obsidianAPI.post(`/vault/tags`, {
    path,
    tags,
    action,
  });
  return response.data.message || 'Tags updated successfully.';
}

/**
 * Performs a search and replace operation within a note.
 * Note: The Obsidian Local REST API might not have a direct endpoint for this.
 * This implementation assumes a hypothetical `/vault/search-replace` endpoint.
 * If not available, this would require reading the note, performing string replacement, and writing back.
 * @param path The path to the note.
 * @param search The string to search for.
 * @param replace The string to replace with.
 * @returns The updated content of the note.
 */
export async function searchReplace(path: string, search: string, replace: string): Promise<string> {
  const response = await obsidianAPI.post<ObsidianNote>(`/vault/search-replace`, {
    path,
    search,
    replace,
  });
  return response.data.content;
}
