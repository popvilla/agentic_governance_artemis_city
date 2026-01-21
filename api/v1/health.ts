/**
 * Health Routes
 *
 * Public endpoints for health checks and status monitoring.
 */

import { Router, Request, Response } from 'express';

const router = Router();

/**
 * GET /health
 * Basic health check
 */
router.get('/', (req: Request, res: Response) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    service: 'Artemis City API',
    version: '1.0.0'
  });
});

/**
 * GET /health/detailed
 * Detailed health check with component status
 */
router.get('/detailed', async (req: Request, res: Response) => {
  const checks = {
    api: 'ok',
    mcp: 'unknown',
    vault: 'unknown',
    agents: 'ok'
  };

  // Check MCP server
  try {
    const mcpResponse = await fetch('http://localhost:3000/health');
    checks.mcp = mcpResponse.ok ? 'ok' : 'degraded';
  } catch {
    checks.mcp = 'unavailable';
  }

  const allOk = Object.values(checks).every(v => v === 'ok');

  res.status(allOk ? 200 : 503).json({
    status: allOk ? 'healthy' : 'degraded',
    timestamp: new Date().toISOString(),
    checks,
    uptime: process.uptime()
  });
});

/**
 * GET /health/ready
 * Readiness probe for orchestration
 */
router.get('/ready', (req: Request, res: Response) => {
  res.status(200).json({ ready: true });
});

/**
 * GET /health/live
 * Liveness probe for orchestration
 */
router.get('/live', (req: Request, res: Response) => {
  res.status(200).json({ alive: true });
});

export default router;
