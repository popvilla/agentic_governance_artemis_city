import { Request, Response, NextFunction } from 'express';
import { MCP_LOG_LEVEL } from '../config';

type LogLevel = 'debug' | 'info' | 'warn' | 'error';

interface Logger {
  debug(message: string, ...meta: unknown[]): void;
  info(message: string, ...meta: unknown[]): void;
  warn(message: string, ...meta: unknown[]): void;
  error(message: string, ...meta: unknown[]): void;
}

const LOG_LEVELS: Record<Uppercase<LogLevel>, number> = {
  DEBUG: 0,
  INFO: 1,
  WARN: 2,
  ERROR: 3,
} as const;

const currentLogLevel = (): number => {
  try {
    const level = MCP_LOG_LEVEL?.toUpperCase() as keyof typeof LOG_LEVELS;
    return level in LOG_LEVELS ? LOG_LEVELS[level] : LOG_LEVELS.INFO;
  } catch (error) {
    console.error('Failed to determine log level, falling back to INFO:', error);
    return LOG_LEVELS.INFO;
  }
};

/**
 * Formats a log message with timestamp and log level
 */
const formatMessage = (level: string, message: string): string => {
  return `[${new Date().toISOString()}] [${level.toUpperCase()}] ${message}`;
};

/**
 * Safely stringifies objects for logging
 */
const safeStringify = (obj: unknown): string => {
  try {
    return JSON.stringify(obj, (_, value) => 
      typeof value === 'bigint' ? value.toString() : value
    );
  } catch (error) {
    return `[Error stringifying log data: ${error instanceof Error ? error.message : String(error)}]`;
  }
};

/**
 * Internal logging function that handles log level filtering and formatting.
 * @private
 */
const log = (level: LogLevel, message: string, ...meta: unknown[]): void => {
  const minLevel = currentLogLevel();
  const levelValue = LOG_LEVELS[level.toUpperCase() as keyof typeof LOG_LEVELS];

  if (levelValue >= minLevel) {
    const formattedMessage = formatMessage(level, message);
    const consoleMethod = console[level] || console.log;
    
    try {
      if (meta.length > 0) {
        const metaString = meta.map(item => 
          typeof item === 'object' ? safeStringify(item) : String(item)
        ).join(' ');
        consoleMethod(`${formattedMessage} - ${metaString}`);
      } else {
        consoleMethod(formattedMessage);
      }
    } catch (error) {
      console.error(`[LOGGER ERROR] Failed to log message: ${error}`);
      console.error(`Original message: ${message}`);
    }
  }
};

/**
 * Logger instance with methods for different log levels.
 * Each method accepts a message and optional metadata.
 * 
 * @example
 * logger.info('Server started', { port: 3000 });
 * logger.error('Database connection failed', { error: err });
 */
export const logger: Logger = {
  debug: (message: string, ...meta: unknown[]) => log('debug', message, ...meta),
  info: (message: string, ...meta: unknown[]) => log('info', message, ...meta),
  warn: (message: string, ...meta: unknown[]) => log('warn', message, ...meta),
  error: (message: string, ...meta: unknown[]) => log('error', message, ...meta),
};

/**
 * Express middleware for logging HTTP requests.
 * Logs method, URL, status code, response time, and IP address.
 * 
 * @example
 * app.use(requestLogger);
 */
export const requestLogger = (req: Request, res: Response, next: NextFunction): void => {
  const start = Date.now();
  
  res.on('finish', () => {
    const duration = Date.now() - start;
    logger.info(
      `${req.method} ${req.originalUrl}`,
      {
        status: res.statusCode,
        duration: `${duration}ms`,
        ip: req.ip,
        userAgent: req.get('user-agent')
      }
    );
  });

  next();
};

/**
 * Error handling middleware that logs errors
 */
export const errorLogger = (err: Error, req: Request, res: Response, next: NextFunction): void => {
  logger.error('Unhandled error', {
    error: err.message,
    stack: process.env.NODE_ENV === 'development' ? err.stack : undefined,
    path: req.path,
    method: req.method,
  });
  
  next(err);
};