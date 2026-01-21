/**
 * LLM API Routes
 *
 * Endpoints for interacting with LLM providers (Claude, OpenAI, etc.)
 */

import { Router, Request, Response } from 'express';
import { LLMController } from '../controllers/llmController';

const router = Router();
const controller = new LLMController();

/**
 * POST /api/v1/llm/chat
 * Send a chat completion request
 */
router.post('/chat', async (req: Request, res: Response) => {
  try {
    const { messages, model, options } = req.body;

    if (!messages || !Array.isArray(messages)) {
      res.status(400).json({
        success: false,
        error: 'messages array is required'
      });
      return;
    }

    const result = await controller.chat(messages, model, options);
    res.json({
      success: true,
      data: result
    });
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * POST /api/v1/llm/complete
 * Send a text completion request
 */
router.post('/complete', async (req: Request, res: Response) => {
  try {
    const { prompt, model, options } = req.body;

    if (!prompt) {
      res.status(400).json({
        success: false,
        error: 'prompt is required'
      });
      return;
    }

    const result = await controller.complete(prompt, model, options);
    res.json({
      success: true,
      data: result
    });
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * POST /api/v1/llm/embed
 * Generate embeddings for text
 */
router.post('/embed', async (req: Request, res: Response) => {
  try {
    const { text, model } = req.body;

    if (!text) {
      res.status(400).json({
        success: false,
        error: 'text is required'
      });
      return;
    }

    const result = await controller.embed(text, model);
    res.json({
      success: true,
      data: result
    });
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * POST /api/v1/llm/stream
 * Stream a chat completion (SSE)
 */
router.post('/stream', async (req: Request, res: Response) => {
  try {
    const { messages, model, options } = req.body;

    if (!messages || !Array.isArray(messages)) {
      res.status(400).json({
        success: false,
        error: 'messages array is required'
      });
      return;
    }

    // Set up SSE headers
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');

    await controller.streamChat(messages, model, options, (chunk) => {
      res.write(`data: ${JSON.stringify(chunk)}\n\n`);
    });

    res.write('data: [DONE]\n\n');
    res.end();
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * GET /api/v1/llm/models
 * List available models
 */
router.get('/models', async (req: Request, res: Response) => {
  try {
    const models = await controller.listModels();
    res.json({
      success: true,
      data: models
    });
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * GET /api/v1/llm/providers
 * List configured providers
 */
router.get('/providers', (req: Request, res: Response) => {
  try {
    const providers = controller.getProviders();
    res.json({
      success: true,
      data: providers
    });
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * POST /api/v1/llm/provider
 * Configure a provider
 */
router.post('/provider', async (req: Request, res: Response) => {
  try {
    const { provider, apiKey, baseUrl, options } = req.body;

    if (!provider) {
      res.status(400).json({
        success: false,
        error: 'provider is required'
      });
      return;
    }

    const result = await controller.configureProvider(provider, { apiKey, baseUrl, ...options });
    res.json({
      success: true,
      data: result,
      message: `Provider ${provider} configured successfully`
    });
  } catch (error: any) {
    res.status(400).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * POST /api/v1/llm/atp
 * Process an ATP message through LLM
 */
router.post('/atp', async (req: Request, res: Response) => {
  try {
    const { atpMessage, model, agentId } = req.body;

    if (!atpMessage) {
      res.status(400).json({
        success: false,
        error: 'atpMessage is required'
      });
      return;
    }

    const result = await controller.processATP(atpMessage, model, agentId);
    res.json({
      success: true,
      data: result
    });
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * GET /api/v1/llm/usage
 * Get token usage statistics
 */
router.get('/usage', async (req: Request, res: Response) => {
  try {
    const { startDate, endDate, provider } = req.query;
    const usage = await controller.getUsage({
      startDate: startDate as string,
      endDate: endDate as string,
      provider: provider as string
    });
    res.json({
      success: true,
      data: usage
    });
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

export default router;
