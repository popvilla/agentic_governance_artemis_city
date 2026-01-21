/**
 * ATP (Artemis Transmission Protocol) Routes
 *
 * Endpoints for sending and processing ATP messages.
 */

import { Router, Request, Response } from 'express';
import { ATPController } from '../controllers/atpController';

const router = Router();
const controller = new ATPController();

/**
 * POST /api/v1/atp/send
 * Send an ATP message for routing
 */
router.post('/send', async (req: Request, res: Response) => {
  try {
    const result = await controller.sendMessage(req.body);
    res.json(result);
  } catch (error: any) {
    res.status(400).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * POST /api/v1/atp/route
 * Route a message to appropriate agent(s)
 */
router.post('/route', async (req: Request, res: Response) => {
  try {
    const { message } = req.body;

    if (!message) {
      res.status(400).json({
        success: false,
        error: 'message is required'
      });
      return;
    }

    const routing = await controller.routeMessage(message);
    res.json({
      success: true,
      data: routing
    });
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * POST /api/v1/atp/validate
 * Validate an ATP message format
 */
router.post('/validate', (req: Request, res: Response) => {
  try {
    const validation = controller.validateMessage(req.body);
    res.json({
      success: true,
      data: validation
    });
  } catch (error: any) {
    res.status(400).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * GET /api/v1/atp/modes
 * Get available ATP modes
 */
router.get('/modes', (req: Request, res: Response) => {
  res.json({
    success: true,
    data: controller.getModes()
  });
});

/**
 * GET /api/v1/atp/priorities
 * Get available ATP priorities
 */
router.get('/priorities', (req: Request, res: Response) => {
  res.json({
    success: true,
    data: controller.getPriorities()
  });
});

/**
 * GET /api/v1/atp/action-types
 * Get available ATP action types
 */
router.get('/action-types', (req: Request, res: Response) => {
  res.json({
    success: true,
    data: controller.getActionTypes()
  });
});

/**
 * GET /api/v1/atp/template
 * Get ATP message template
 */
router.get('/template', (req: Request, res: Response) => {
  res.json({
    success: true,
    data: {
      template: {
        header: {
          mode: 'QUERY',
          context: 'Brief description of the task',
          priority: 'MEDIUM',
          actionType: 'READ',
          targetZone: 'system',
          specialNotes: 'Optional special instructions',
          senderId: 'your-agent-id'
        },
        payload: {
          content: 'Main message content'
        }
      },
      requiredFields: ['header.mode', 'header.context', 'payload'],
      optionalFields: ['header.priority', 'header.actionType', 'header.targetZone', 'header.specialNotes']
    }
  });
});

/**
 * POST /api/v1/atp/format
 * Format content as ATP message (returns formatted string)
 */
router.post('/format', async (req: Request, res: Response) => {
  try {
    // First validate and send to get a complete message
    const sendResult = await controller.sendMessage(req.body);

    if (!sendResult.success) {
      res.status(400).json(sendResult);
      return;
    }

    // Get the message back and format it
    const message = controller.getMessage(sendResult.messageId);
    if (!message) {
      res.status(404).json({
        success: false,
        error: 'Message not found after creation'
      });
      return;
    }

    const formatted = controller.formatMessage(message);
    res.json({
      success: true,
      data: {
        message,
        formatted
      }
    });
  } catch (error: any) {
    res.status(400).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * GET /api/v1/atp/message/:id
 * Get a message by ID
 */
router.get('/message/:id', (req: Request, res: Response) => {
  try {
    const message = controller.getMessage(req.params.id);

    if (!message) {
      res.status(404).json({
        success: false,
        error: `Message not found: ${req.params.id}`
      });
      return;
    }

    res.json({
      success: true,
      data: message
    });
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * GET /api/v1/atp/response/:id
 * Get response for a message
 */
router.get('/response/:id', (req: Request, res: Response) => {
  try {
    const response = controller.getResponse(req.params.id);

    if (!response) {
      res.status(404).json({
        success: false,
        error: `Response not found for message: ${req.params.id}`
      });
      return;
    }

    res.json({
      success: true,
      data: response
    });
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * GET /api/v1/atp/queue
 * Get message queue status
 */
router.get('/queue', (req: Request, res: Response) => {
  try {
    const status = controller.getQueueStatus();
    res.json({
      success: true,
      data: status
    });
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

export default router;
