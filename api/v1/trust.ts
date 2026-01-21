/**
 * Trust Routes
 *
 * Endpoints for trust management and Hebbian learning.
 */

import { Router, Request, Response } from 'express';
import { TrustController } from '../controllers/trustController';

const router = Router();
const controller = new TrustController();

/**
 * GET /api/v1/trust/report
 * Get comprehensive trust report
 */
router.get('/report', async (req: Request, res: Response) => {
  try {
    const report = await controller.getTrustReport();
    res.json({
      success: true,
      data: report
    });
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * GET /api/v1/trust/:entityId
 * Get trust score for an entity
 */
router.get('/:entityId', async (req: Request, res: Response) => {
  try {
    const { entityId } = req.params;
    const trust = await controller.getTrustScore(entityId);

    if (trust === null) {
      res.status(404).json({
        success: false,
        error: `Entity not found: ${entityId}`
      });
      return;
    }

    res.json({
      success: true,
      data: trust
    });
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * PUT /api/v1/trust/:entityId
 * Set trust score for an entity
 */
router.put('/:entityId', async (req: Request, res: Response) => {
  try {
    const { entityId } = req.params;
    const { score, entityType = 'agent' } = req.body;

    if (typeof score !== 'number' || score < 0 || score > 1) {
      res.status(400).json({
        success: false,
        error: 'score must be a number between 0 and 1'
      });
      return;
    }

    const result = await controller.setTrustScore(entityId, score, entityType);
    res.json({
      success: true,
      data: result,
      message: 'Trust score updated'
    });
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * POST /api/v1/trust/:entityId/success
 * Record successful operation
 */
router.post('/:entityId/success', async (req: Request, res: Response) => {
  try {
    const { entityId } = req.params;
    const { amount = 0.02 } = req.body;

    const newScore = await controller.recordSuccess(entityId, amount);

    if (newScore === null) {
      res.status(404).json({
        success: false,
        error: `Entity not found: ${entityId}`
      });
      return;
    }

    res.json({
      success: true,
      data: { entityId, newScore, delta: amount },
      message: 'Success recorded'
    });
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * POST /api/v1/trust/:entityId/failure
 * Record failed operation
 */
router.post('/:entityId/failure', async (req: Request, res: Response) => {
  try {
    const { entityId } = req.params;
    const { amount = 0.05 } = req.body;

    const newScore = await controller.recordFailure(entityId, amount);

    if (newScore === null) {
      res.status(404).json({
        success: false,
        error: `Entity not found: ${entityId}`
      });
      return;
    }

    res.json({
      success: true,
      data: { entityId, newScore, delta: -amount },
      message: 'Failure recorded'
    });
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * GET /api/v1/trust/:entityId/permissions
 * Check what operations an entity can perform
 */
router.get('/:entityId/permissions', async (req: Request, res: Response) => {
  try {
    const { entityId } = req.params;
    const permissions = await controller.getPermissions(entityId);

    res.json({
      success: true,
      data: permissions
    });
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * POST /api/v1/trust/:entityId/can-perform
 * Check if entity can perform specific operation
 */
router.post('/:entityId/can-perform', async (req: Request, res: Response) => {
  try {
    const { entityId } = req.params;
    const { operation } = req.body;

    if (!operation) {
      res.status(400).json({
        success: false,
        error: 'operation is required'
      });
      return;
    }

    const canPerform = await controller.canPerformOperation(entityId, operation);
    res.json({
      success: true,
      data: {
        entityId,
        operation,
        allowed: canPerform
      }
    });
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * GET /api/v1/trust/hebbian/weights
 * Get Hebbian connection weights
 */
router.get('/hebbian/weights', async (req: Request, res: Response) => {
  try {
    const weights = await controller.getHebbianWeights();
    res.json({
      success: true,
      data: weights
    });
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * PUT /api/v1/trust/hebbian/weights
 * Update Hebbian connection weight
 */
router.put('/hebbian/weights', async (req: Request, res: Response) => {
  try {
    const { agent1, agent2, delta } = req.body;

    if (!agent1 || !agent2 || typeof delta !== 'number') {
      res.status(400).json({
        success: false,
        error: 'agent1, agent2, and delta are required'
      });
      return;
    }

    const newWeight = await controller.updateHebbianWeight(agent1, agent2, delta);
    res.json({
      success: true,
      data: {
        connection: `${agent1}-${agent2}`,
        newWeight,
        delta
      },
      message: 'Hebbian weight updated'
    });
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * GET /api/v1/trust/levels
 * Get trust level definitions
 */
router.get('/levels', (req: Request, res: Response) => {
  res.json({
    success: true,
    data: {
      levels: [
        { name: 'FULL', range: '0.9 - 1.0', operations: ['read', 'write', 'delete', 'search', 'tag', 'update', 'frontmatter'] },
        { name: 'HIGH', range: '0.7 - 0.9', operations: ['read', 'write', 'search', 'tag', 'update', 'frontmatter'] },
        { name: 'MEDIUM', range: '0.5 - 0.7', operations: ['read', 'write', 'search', 'tag'] },
        { name: 'LOW', range: '0.3 - 0.5', operations: ['read', 'search'] },
        { name: 'UNTRUSTED', range: '0.0 - 0.3', operations: [] }
      ],
      decayRate: '1% per day',
      reinforcement: '+0.02 per success',
      penalty: '-0.05 per failure'
    }
  });
});

export default router;
