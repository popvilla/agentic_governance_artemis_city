/**
 * Artemis City API
 *
 * Main entry point for the Artemis City REST API.
 * Provides endpoints for agent coordination, memory operations, and ATP messaging.
 *
 * Author: Prinston Palmer
 * Version: 1.0.0
 */

import express, { Express, Request, Response, NextFunction } from 'express';
import cors from 'cors';
import helmet from 'helmet';

// Routes
import agentRoutes from './routes/agents';
import memoryRoutes from './routes/memory';
import atpRoutes from './routes/atp';
import trustRoutes from './routes/trust';
import healthRoutes from './routes/health';
import llmRoutes from './routes/llm';

// Middleware
import { authMiddleware } from './middleware/auth';
import { errorHandler } from './middleware/errorHandler';
import { requestLogger } from './middleware/logger';

// Config
const PORT = process.env.API_PORT || 4000;
const API_VERSION = 'v1';

// Initialize Express app
const app: Express = express();

// ============================================================================
// Global Middleware
// ============================================================================

app.use(helmet());
app.use(cors());
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));
app.use(requestLogger);

// ============================================================================
// Routes
// ============================================================================

// Public routes (no auth)
app.use('/health', healthRoutes);
app.use(`/api/${API_VERSION}/health`, healthRoutes);

// Protected routes (require auth)
app.use(`/api/${API_VERSION}/agents`, authMiddleware, agentRoutes);
app.use(`/api/${API_VERSION}/memory`, authMiddleware, memoryRoutes);
app.use(`/api/${API_VERSION}/atp`, authMiddleware, atpRoutes);
app.use(`/api/${API_VERSION}/trust`, authMiddleware, trustRoutes);
app.use(`/api/${API_VERSION}/llm`, authMiddleware, llmRoutes);

// API documentation endpoint
app.get(`/api/${API_VERSION}`, (req: Request, res: Response) => {
  res.json({
    name: 'Artemis City API',
    version: '1.0.0',
    apiVersion: API_VERSION,
    endpoints: {
      health: '/health',
      agents: `/api/${API_VERSION}/agents`,
      memory: `/api/${API_VERSION}/memory`,
      atp: `/api/${API_VERSION}/atp`,
      trust: `/api/${API_VERSION}/trust`,
      llm: `/api/${API_VERSION}/llm`
    },
    documentation: `/api/${API_VERSION}/docs`
  });
});

// 404 handler
app.use((req: Request, res: Response) => {
  res.status(404).json({
    success: false,
    error: 'Endpoint not found',
    path: req.path
  });
});

// Error handler
app.use(errorHandler);

// ============================================================================
// Server Start
// ============================================================================

export function startServer(): void {
  app.listen(PORT, () => {
    console.log('='.repeat(50));
    console.log('Artemis City API Server');
    console.log('='.repeat(50));
    console.log(`Server running on http://localhost:${PORT}`);
    console.log(`API endpoint: http://localhost:${PORT}/api/${API_VERSION}`);
    console.log(`Health check: http://localhost:${PORT}/health`);
    console.log('='.repeat(50));
  });
}

export { app };

// Start if run directly
if (require.main === module) {
  startServer();
}
