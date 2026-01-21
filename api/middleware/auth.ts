/**
 * Authentication Middleware
 *
 * Handles API authentication and authorization.
 */

import { Request, Response, NextFunction } from 'express';

interface AuthenticatedRequest extends Request {
  user?: {
    id: string;
    role: string;
    permissions: string[];
  };
  apiKey?: string;
}

// API key store (in production, use database or secure vault)
const API_KEYS: Record<string, { userId: string; role: string; permissions: string[] }> = {
  'artemis-key-001': {
    userId: 'artemis',
    role: 'admin',
    permissions: ['read', 'write', 'delete', 'admin']
  },
  'packrat-key-001': {
    userId: 'packrat',
    role: 'service',
    permissions: ['read', 'write', 'search']
  },
  'copilot-key-001': {
    userId: 'copilot',
    role: 'assistant',
    permissions: ['read', 'search', 'query']
  },
  'daemon-key-001': {
    userId: 'daemon',
    role: 'service',
    permissions: ['read', 'write', 'system']
  },
  'dev-key-local': {
    userId: 'developer',
    role: 'admin',
    permissions: ['read', 'write', 'delete', 'admin']
  }
};

/**
 * Main authentication middleware
 */
export const authMiddleware = (req: AuthenticatedRequest, res: Response, next: NextFunction): void => {
  // Skip auth in development mode
  if (process.env.NODE_ENV === 'development' && process.env.SKIP_AUTH === 'true') {
    req.user = {
      id: 'dev-user',
      role: 'admin',
      permissions: ['read', 'write', 'delete', 'admin']
    };
    next();
    return;
  }

  // Extract API key from header
  const authHeader = req.headers.authorization;
  const apiKey = req.headers['x-api-key'] as string;

  let key: string | undefined;

  if (authHeader?.startsWith('Bearer ')) {
    key = authHeader.substring(7);
  } else if (apiKey) {
    key = apiKey;
  }

  if (!key) {
    res.status(401).json({
      success: false,
      error: 'Authentication required',
      message: 'Please provide an API key via Authorization header (Bearer token) or X-API-Key header'
    });
    return;
  }

  // Validate API key
  const keyData = API_KEYS[key];
  if (!keyData) {
    res.status(401).json({
      success: false,
      error: 'Invalid API key',
      message: 'The provided API key is not valid'
    });
    return;
  }

  // Attach user info to request
  req.user = {
    id: keyData.userId,
    role: keyData.role,
    permissions: keyData.permissions
  };
  req.apiKey = key;

  next();
};

/**
 * Permission check middleware factory
 */
export const requirePermission = (permission: string) => {
  return (req: AuthenticatedRequest, res: Response, next: NextFunction): void => {
    if (!req.user) {
      res.status(401).json({
        success: false,
        error: 'Authentication required'
      });
      return;
    }

    if (!req.user.permissions.includes(permission) && !req.user.permissions.includes('admin')) {
      res.status(403).json({
        success: false,
        error: 'Permission denied',
        message: `This action requires '${permission}' permission`
      });
      return;
    }

    next();
  };
};

/**
 * Role check middleware factory
 */
export const requireRole = (...roles: string[]) => {
  return (req: AuthenticatedRequest, res: Response, next: NextFunction): void => {
    if (!req.user) {
      res.status(401).json({
        success: false,
        error: 'Authentication required'
      });
      return;
    }

    if (!roles.includes(req.user.role)) {
      res.status(403).json({
        success: false,
        error: 'Role not authorized',
        message: `This action requires one of these roles: ${roles.join(', ')}`
      });
      return;
    }

    next();
  };
};

/**
 * Rate limiting state
 */
const rateLimitStore: Map<string, { count: number; resetTime: number }> = new Map();

/**
 * Rate limiting middleware
 */
export const rateLimit = (options: { windowMs?: number; maxRequests?: number } = {}) => {
  const windowMs = options.windowMs || 60000; // 1 minute default
  const maxRequests = options.maxRequests || 100; // 100 requests per window

  return (req: AuthenticatedRequest, res: Response, next: NextFunction): void => {
    const key = req.apiKey || req.ip || 'anonymous';
    const now = Date.now();

    let record = rateLimitStore.get(key);

    if (!record || now > record.resetTime) {
      record = { count: 0, resetTime: now + windowMs };
    }

    record.count++;
    rateLimitStore.set(key, record);

    // Set rate limit headers
    res.setHeader('X-RateLimit-Limit', maxRequests.toString());
    res.setHeader('X-RateLimit-Remaining', Math.max(0, maxRequests - record.count).toString());
    res.setHeader('X-RateLimit-Reset', record.resetTime.toString());

    if (record.count > maxRequests) {
      res.status(429).json({
        success: false,
        error: 'Rate limit exceeded',
        message: `Too many requests. Please try again after ${Math.ceil((record.resetTime - now) / 1000)} seconds`
      });
      return;
    }

    next();
  };
};

export default authMiddleware;
