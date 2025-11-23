import { Request, Response, NextFunction } from 'express';
import { MCP_API_KEY } from '../../config';
import { logger } from '../../utils/logger';

/**
 * Middleware to authenticate requests using a Bearer token.
 * It checks for an 'Authorization' header with a 'Bearer' token
 * and validates it against the configured MCP_API_KEY.
 *
 * @param req The Express request object.
 * @param res The Express response object.
 * @param next The next middleware function in the stack.
 * @returns void
 */
export const authenticateMCP = (req: Request, res: Response, next: NextFunction): void => {
  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    logger.warn('Authentication failed: Missing or malformed Bearer token.');
    return res.status(401).json({ success: false, error: 'Unauthorized: Bearer token required.' });
  }

  const token = authHeader.split(' ')[1];

  // Ensure MCP_API_KEY is not empty, though config validation should prevent this.
  if (!MCP_API_KEY) {
    logger.error('Server configuration error: MCP_API_KEY is not set.');
    return res.status(500).json({ success: false, error: 'Server configuration error.' });
  }

  if (token === MCP_API_KEY) {
    logger.debug('Authentication successful for incoming request.');
    next();
  } else {
    logger.warn('Authentication failed: Invalid MCP_API_KEY provided.');
    return res.status(403).json({ success: false, error: 'Forbidden: Invalid API Key.' });
  }
};