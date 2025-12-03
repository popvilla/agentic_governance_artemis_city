import { Router } from 'express';
import { authenticateMCP } from './middleware/auth';
import { getContext } from './tools/obsidianReadNoteTool';
import { appendContext, updateNote } from './tools/obsidianUpdateNoteTool';
import { searchNotes } from './tools/obsidianGlobalSearchTool';
import { listNotes } from './tools/obsidianListNotesTool';
import { deleteNote } from './tools/obsidianDeleteNoteTool';
import { manageFrontmatter } from './tools/obsidianManageFrontmatterTool';
import { manageTags } from './tools/obsidianManageTagsTool';
import { searchReplace } from './tools/obsidianSearchReplaceTool';
import { logger } from '../utils/logger';

const mcpRouter = Router();

// All MCP routes require authentication
mcpRouter.use(authenticateMCP);

// Define MCP endpoints
mcpRouter.post('/getContext', async (req, res) => {
  const { path } = req.body;
  if (!path) {
    return res.status(400).json({ success: false, error: 'Missing note path.' });
  }
  logger.debug(`Received getContext request for path: ${path}`);
  const result = await getContext(path);
  res.status(result.success ? 200 : 500).json(result);
});

mcpRouter.post('/appendContext', async (req, res) => {
  const { path, content } = req.body;
  if (!path || content === undefined) {
    return res.status(400).json({ success: false, error: 'Missing note path or content.' });
  }
  logger.debug(`Received appendContext request for path: ${path}`);
  const result = await appendContext(path, content);
  res.status(result.success ? 200 : 500).json(result);
});

mcpRouter.post('/updateNote', async (req, res) => {
  const { path, content } = req.body;
  if (!path || content === undefined) {
    return res.status(400).json({ success: false, error: 'Missing note path or content.' });
  }
  logger.debug(`Received updateNote request for path: ${path}`);
  const result = await updateNote(path, content);
  res.status(result.success ? 200 : 500).json(result);
});

mcpRouter.post('/searchNotes', async (req, res) => {
  const { query } = req.body;
  if (!query) {
    return res.status(400).json({ success: false, error: 'Missing search query.' });
  }
  logger.debug(`Received searchNotes request for query: ${query}`);
  const result = await searchNotes(query);
  res.status(result.success ? 200 : 500).json(result);
});

mcpRouter.post('/listNotes', async (req, res) => {
  logger.debug('Received listNotes request.');
  const result = await listNotes();
  res.status(result.success ? 200 : 500).json(result);
});

mcpRouter.post('/deleteNote', async (req, res) => {
  const { path } = req.body;
  if (!path) {
    return res.status(400).json({ success: false, error: 'Missing note path.' });
  }
  logger.debug(`Received deleteNote request for path: ${path}`);
  const result = await deleteNote(path);
  res.status(result.success ? 200 : 500).json(result);
});

mcpRouter.post('/manageFrontmatter', async (req, res) => {
  const { path, key, value } = req.body;
  if (!path || !key || value === undefined) {
    return res.status(400).json({ success: false, error: 'Missing note path, frontmatter key, or value.' });
  }
  logger.debug(`Received manageFrontmatter request for path: ${path}, key: ${key}`);
  const result = await manageFrontmatter(path, key, value);
  res.status(result.success ? 200 : 500).json(result);
});

mcpRouter.post('/manageTags', async (req, res) => {
  const { path, tags, action } = req.body;
  if (!path || !Array.isArray(tags) || !['add', 'remove'].includes(action)) {
    return res.status(400).json({ success: false, error: 'Missing note path, tags (array), or invalid action (add/remove).' });
  }
  logger.debug(`Received manageTags request for path: ${path}, action: ${action}, tags: ${tags.join(', ')}`);
  const result = await manageTags(path, tags, action);
  res.status(result.success ? 200 : 500).json(result);
});

mcpRouter.post('/searchReplace', async (req, res) => {
  const { path, search, replace } = req.body;
  if (!path || !search || replace === undefined) {
    return res.status(400).json({ success: false, error: 'Missing note path, search string, or replace string.' });
  }
  logger.debug(`Received searchReplace request for path: ${path}, search: ${search}`);
  const result = await searchReplace(path, search, replace);
  res.status(result.success ? 200 : 500).json(result);
});

export { mcpRouter };
