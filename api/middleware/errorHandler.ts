/**
 * Error Handler Middleware
 *
 * Centralized error handling for the API.
 */

import { Request, Response, NextFunction } from 'express';

/**
 * Custom API Error class
 */
export class APIError extends Error {
  statusCode: number;
  code: string;
  details?: any;

  constructor(message: string, statusCode: number = 500, code: string = 'INTERNAL_ERROR', details?: any) {
    super(message);
    this.name = 'APIError';
    this.statusCode = statusCode;
    this.code = code;
    this.details = details;
  }
}

/**
 * Predefined error types
 */
export const Errors = {
  NotFound: (resource: string) =>
    new APIError(`${resource} not found`, 404, 'NOT_FOUND'),

  BadRequest: (message: string, details?: any) =>
    new APIError(message, 400, 'BAD_REQUEST', details),

  Unauthorized: (message: string = 'Authentication required') =>
    new APIError(message, 401, 'UNAUTHORIZED'),

  Forbidden: (message: string = 'Permission denied') =>
    new APIError(message, 403, 'FORBIDDEN'),

  Conflict: (message: string) =>
    new APIError(message, 409, 'CONFLICT'),

  ValidationError: (errors: any[]) =>
    new APIError('Validation failed', 400, 'VALIDATION_ERROR', { errors }),

  RateLimited: () =>
    new APIError('Too many requests', 429, 'RATE_LIMITED'),

  InternalError: (message: string = 'Internal server error') =>
    new APIError(message, 500, 'INTERNAL_ERROR')
};

/**
 * Error response interface
 */
interface ErrorResponse {
  success: false;
  error: {
    message: string;
    code: string;
    statusCode: number;
    details?: any;
    timestamp: string;
    path?: string;
    requestId?: string;
  };
}

/**
 * Main error handler middleware
 */
export const errorHandler = (
  err: Error | APIError,
  req: Request,
  res: Response,
  next: NextFunction
): void => {
  // Log error
  console.error(`[ERROR] ${new Date().toISOString()} - ${req.method} ${req.path}`);
  console.error(err.stack || err.message);

  // Determine status code and error details
  let statusCode = 500;
  let code = 'INTERNAL_ERROR';
  let message = 'An unexpected error occurred';
  let details: any = undefined;

  if (err instanceof APIError) {
    statusCode = err.statusCode;
    code = err.code;
    message = err.message;
    details = err.details;
  } else if (err.name === 'ValidationError') {
    statusCode = 400;
    code = 'VALIDATION_ERROR';
    message = err.message;
  } else if (err.name === 'SyntaxError' && 'body' in err) {
    statusCode = 400;
    code = 'INVALID_JSON';
    message = 'Invalid JSON in request body';
  } else if (err.name === 'UnauthorizedError') {
    statusCode = 401;
    code = 'UNAUTHORIZED';
    message = 'Invalid or expired token';
  }

  // Build error response
  const errorResponse: ErrorResponse = {
    success: false,
    error: {
      message,
      code,
      statusCode,
      timestamp: new Date().toISOString(),
      path: req.path
    }
  };

  // Include details in development mode
  if (process.env.NODE_ENV === 'development') {
    errorResponse.error.details = details || {
      stack: err.stack?.split('\n').slice(0, 5)
    };
  } else if (details && code === 'VALIDATION_ERROR') {
    // Always include validation errors
    errorResponse.error.details = details;
  }

  res.status(statusCode).json(errorResponse);
};

/**
 * Not found handler for unmatched routes
 */
export const notFoundHandler = (req: Request, res: Response): void => {
  res.status(404).json({
    success: false,
    error: {
      message: `Route not found: ${req.method} ${req.path}`,
      code: 'ROUTE_NOT_FOUND',
      statusCode: 404,
      timestamp: new Date().toISOString(),
      path: req.path
    }
  });
};

/**
 * Async handler wrapper to catch async errors
 */
export const asyncHandler = (fn: (req: Request, res: Response, next: NextFunction) => Promise<any>) => {
  return (req: Request, res: Response, next: NextFunction): void => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
};

export default errorHandler;
