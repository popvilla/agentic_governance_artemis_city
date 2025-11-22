import 'dotenv/config'; // Load environment variables first
import express from 'express';
import cors from 'cors';
import { PORT } from './config';
import { mcpRouter } from './mcp-server';
import { requestLogger, logger } from './utils/logger';

const app = express();

// Middleware
app.use(cors());
app.use(express.json());
app.use(requestLogger);

// Routes
app.use('/api', mcpRouter);

// Basic health check endpoint
app.get('/health', (req, res) => {
  res.status(200).send('MCP Server is healthy!');
});

// Start the server
app.listen(PORT, () => {
  logger.info(`MCP Server running on port ${PORT}`);
  logger.info(`Access at http://localhost:${PORT}`);
});
