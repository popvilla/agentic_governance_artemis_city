/**
 * Agent Routes
 *
 * Endpoints for agent registry operations.
 */

import { Router, Request, Response } from 'express';
import { AgentController } from '../controllers/agentController';

const router = Router();
const controller = new AgentController();

/**
 * GET /api/v1/agents
 * List all registered agents
 */
router.get('/', async (req: Request, res: Response) => {
  try {
    const agents = await controller.getAllAgents();
    res.json({
      success: true,
      data: agents,
      count: agents.length
    });
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * GET /api/v1/agents/:id
 * Get agent by ID
 */
router.get('/:id', async (req: Request, res: Response) => {
  try {
    const agent = await controller.getAgent(req.params.id);
    if (!agent) {
      res.status(404).json({
        success: false,
        error: `Agent not found: ${req.params.id}`
      });
      return;
    }
    res.json({
      success: true,
      data: agent
    });
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * POST /api/v1/agents
 * Register a new agent
 */
router.post('/', async (req: Request, res: Response) => {
  try {
    const agent = await controller.registerAgent(req.body);
    res.status(201).json({
      success: true,
      data: agent,
      message: 'Agent registered successfully'
    });
  } catch (error: any) {
    res.status(400).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * PUT /api/v1/agents/:id
 * Update an agent
 */
router.put('/:id', async (req: Request, res: Response) => {
  try {
    const agent = await controller.updateAgent(req.params.id, req.body);
    if (!agent) {
      res.status(404).json({
        success: false,
        error: `Agent not found: ${req.params.id}`
      });
      return;
    }
    res.json({
      success: true,
      data: agent,
      message: 'Agent updated successfully'
    });
  } catch (error: any) {
    res.status(400).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * DELETE /api/v1/agents/:id
 * Unregister an agent
 */
router.delete('/:id', async (req: Request, res: Response) => {
  try {
    const success = await controller.deleteAgent(req.params.id);
    if (!success) {
      res.status(404).json({
        success: false,
        error: `Agent not found: ${req.params.id}`
      });
      return;
    }
    res.json({
      success: true,
      message: 'Agent unregistered successfully'
    });
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * POST /api/v1/agents/:id/suspend
 * Suspend an agent
 */
router.post('/:id/suspend', async (req: Request, res: Response) => {
  try {
    const { reason } = req.body;
    const success = await controller.suspendAgent(req.params.id, reason);
    if (!success) {
      res.status(404).json({
        success: false,
        error: `Agent not found: ${req.params.id}`
      });
      return;
    }
    res.json({
      success: true,
      message: `Agent suspended: ${reason || 'No reason provided'}`
    });
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * POST /api/v1/agents/:id/activate
 * Activate an agent
 */
router.post('/:id/activate', async (req: Request, res: Response) => {
  try {
    const success = await controller.activateAgent(req.params.id);
    if (!success) {
      res.status(404).json({
        success: false,
        error: `Agent not found: ${req.params.id}`
      });
      return;
    }
    res.json({
      success: true,
      message: 'Agent activated successfully'
    });
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * GET /api/v1/agents/:id/card
 * Get agent card (markdown format)
 */
router.get('/:id/card', async (req: Request, res: Response) => {
  try {
    const card = await controller.getAgentCard(req.params.id);
    if (!card) {
      res.status(404).json({
        success: false,
        error: `Agent not found: ${req.params.id}`
      });
      return;
    }

    if (req.query.format === 'markdown') {
      res.type('text/markdown').send(card);
    } else {
      res.json({
        success: true,
        data: { markdown: card }
      });
    }
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

export default router;
