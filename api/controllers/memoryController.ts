/**
 * Memory Controller
 *
 * Handles business logic for memory/vault operations.
 */

import * as fs from 'fs/promises';
import * as path from 'path';

interface MemoryEntry {
  path: string;
  content: string;
  metadata: Record<string, any>;
  createdAt: string;
  updatedAt: string;
}

interface SearchResult {
  path: string;
  matches: string[];
  score: number;
}

interface ContextData {
  recentFiles: string[];
  activeTopics: string[];
  sessionContext: Record<string, any>;
}

// In-memory store for demo (would connect to actual vault in production)
const memoryStore: Map<string, MemoryEntry> = new Map();
const contextStore: ContextData = {
  recentFiles: [],
  activeTopics: [],
  sessionContext: {}
};

// Initialize with sample data
const sampleEntries: MemoryEntry[] = [
  {
    path: 'journal/2026-01-21.md',
    content: '# Daily Journal\n\nToday we built the Artemis City API...',
    metadata: { type: 'journal', tags: ['daily', 'development'] },
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  },
  {
    path: 'agents/registry.md',
    content: '# Agent Registry\n\nCore agents: Artemis, PackRat, Copilot, Daemon',
    metadata: { type: 'reference', tags: ['agents', 'registry'] },
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  },
  {
    path: 'protocols/atp.md',
    content: '# Artemis Transmission Protocol\n\nStructured communication for agents...',
    metadata: { type: 'protocol', tags: ['atp', 'communication'] },
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  }
];

sampleEntries.forEach(entry => memoryStore.set(entry.path, entry));

export class MemoryController {
  private vaultPath: string;

  constructor() {
    this.vaultPath = process.env.OBSIDIAN_VAULT_PATH || '/vault';
  }

  /**
   * Read a file from the vault
   */
  async readFile(filePath: string): Promise<MemoryEntry | null> {
    // Check in-memory store first
    if (memoryStore.has(filePath)) {
      this.updateContext(filePath, 'read');
      return memoryStore.get(filePath)!;
    }

    // Try to read from actual vault
    try {
      const fullPath = path.join(this.vaultPath, filePath);
      const content = await fs.readFile(fullPath, 'utf-8');

      const entry: MemoryEntry = {
        path: filePath,
        content,
        metadata: await this.extractMetadata(content),
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      };

      memoryStore.set(filePath, entry);
      this.updateContext(filePath, 'read');
      return entry;
    } catch (error) {
      return null;
    }
  }

  /**
   * Write content to the vault
   */
  async writeFile(filePath: string, content: string, metadata?: Record<string, any>): Promise<MemoryEntry> {
    const now = new Date().toISOString();
    const existing = memoryStore.get(filePath);

    const entry: MemoryEntry = {
      path: filePath,
      content,
      metadata: metadata || await this.extractMetadata(content),
      createdAt: existing?.createdAt || now,
      updatedAt: now
    };

    memoryStore.set(filePath, entry);
    this.updateContext(filePath, 'write');

    // Try to write to actual vault
    try {
      const fullPath = path.join(this.vaultPath, filePath);
      await fs.mkdir(path.dirname(fullPath), { recursive: true });
      await fs.writeFile(fullPath, content, 'utf-8');
    } catch (error) {
      // Store in memory if file system write fails
      console.warn(`Could not write to vault: ${error}`);
    }

    return entry;
  }

  /**
   * Delete a file from the vault
   */
  async deleteFile(filePath: string): Promise<boolean> {
    const deleted = memoryStore.delete(filePath);

    // Try to delete from actual vault
    try {
      const fullPath = path.join(this.vaultPath, filePath);
      await fs.unlink(fullPath);
    } catch (error) {
      // Ignore file system errors
    }

    return deleted;
  }

  /**
   * Search the vault
   */
  async search(query: string, options?: { path?: string; tags?: string[]; limit?: number }): Promise<SearchResult[]> {
    const results: SearchResult[] = [];
    const limit = options?.limit || 10;
    const queryLower = query.toLowerCase();

    for (const [filePath, entry] of memoryStore) {
      // Filter by path if specified
      if (options?.path && !filePath.startsWith(options.path)) {
        continue;
      }

      // Filter by tags if specified
      if (options?.tags && options.tags.length > 0) {
        const entryTags = entry.metadata.tags || [];
        if (!options.tags.some(tag => entryTags.includes(tag))) {
          continue;
        }
      }

      // Search in content
      const contentLower = entry.content.toLowerCase();
      const matches: string[] = [];
      let score = 0;

      // Find matching lines
      const lines = entry.content.split('\n');
      for (const line of lines) {
        if (line.toLowerCase().includes(queryLower)) {
          matches.push(line.trim());
          score += 1;
        }
      }

      // Check filename
      if (filePath.toLowerCase().includes(queryLower)) {
        score += 5;
      }

      if (score > 0) {
        results.push({
          path: filePath,
          matches: matches.slice(0, 3),
          score
        });
      }
    }

    // Sort by score and limit
    return results
      .sort((a, b) => b.score - a.score)
      .slice(0, limit);
  }

  /**
   * List files in a directory
   */
  async listFiles(dirPath: string = ''): Promise<string[]> {
    const files: string[] = [];

    for (const filePath of memoryStore.keys()) {
      if (dirPath === '' || filePath.startsWith(dirPath)) {
        files.push(filePath);
      }
    }

    // Try to list from actual vault
    try {
      const fullPath = path.join(this.vaultPath, dirPath);
      const entries = await fs.readdir(fullPath, { withFileTypes: true });

      for (const entry of entries) {
        const relativePath = path.join(dirPath, entry.name);
        if (!files.includes(relativePath)) {
          files.push(relativePath);
        }
      }
    } catch (error) {
      // Use memory store only
    }

    return files.sort();
  }

  /**
   * Get current context
   */
  async getContext(): Promise<ContextData> {
    return { ...contextStore };
  }

  /**
   * Update context
   */
  async updateContextData(key: string, value: any): Promise<ContextData> {
    contextStore.sessionContext[key] = value;
    return this.getContext();
  }

  /**
   * Clear context
   */
  async clearContext(): Promise<void> {
    contextStore.recentFiles = [];
    contextStore.activeTopics = [];
    contextStore.sessionContext = {};
  }

  /**
   * Get vault statistics
   */
  async getStats(): Promise<Record<string, any>> {
    const files = Array.from(memoryStore.values());
    const totalSize = files.reduce((sum, f) => sum + f.content.length, 0);

    const typeCount: Record<string, number> = {};
    files.forEach(f => {
      const type = f.metadata.type || 'unknown';
      typeCount[type] = (typeCount[type] || 0) + 1;
    });

    return {
      totalFiles: files.length,
      totalSize,
      averageSize: Math.round(totalSize / files.length) || 0,
      byType: typeCount,
      recentActivity: contextStore.recentFiles.slice(0, 5)
    };
  }

  // Helper methods
  private async extractMetadata(content: string): Promise<Record<string, any>> {
    const metadata: Record<string, any> = {};

    // Extract YAML frontmatter if present
    const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
    if (frontmatterMatch) {
      const yaml = frontmatterMatch[1];
      // Simple YAML parsing
      yaml.split('\n').forEach(line => {
        const [key, ...valueParts] = line.split(':');
        if (key && valueParts.length > 0) {
          const value = valueParts.join(':').trim();
          if (value.startsWith('[') && value.endsWith(']')) {
            metadata[key.trim()] = value.slice(1, -1).split(',').map(v => v.trim());
          } else {
            metadata[key.trim()] = value;
          }
        }
      });
    }

    // Extract tags from content
    const tagMatches = content.match(/#[\w-]+/g);
    if (tagMatches) {
      metadata.inlineTags = [...new Set(tagMatches.map(t => t.slice(1)))];
    }

    return metadata;
  }

  private updateContext(filePath: string, operation: string): void {
    // Update recent files
    contextStore.recentFiles = [filePath, ...contextStore.recentFiles.filter(f => f !== filePath)].slice(0, 20);

    // Extract topics from path
    const pathParts = filePath.split('/');
    if (pathParts.length > 1) {
      const topic = pathParts[0];
      if (!contextStore.activeTopics.includes(topic)) {
        contextStore.activeTopics = [topic, ...contextStore.activeTopics].slice(0, 10);
      }
    }
  }
}
