import { Request, Response, NextFunction } from 'express';
import { MCP_LOG_LEVEL } from '../config';

// Use a const enum for better tree-shaking and performance.
// The values are explicitly assigned for clarity and to ensure numerical order.
const enum LogLevel {
  DEBUG = 0,
  INFO = 1,
  WARN = 2,
  ERROR = 3,
}

// Determine the current logging level from environment configuration.
// MCP_LOG_LEVEL is guaranteed to be one of 'debug', 'info', 'warn', 'error' by config validation.
// Using .toUpperCase() to match enum keys. The 'as keyof typeof LogLevel' cast is safe
// because MCP_LOG_LEVEL is strictly typed in config/index.ts.
const currentLogLevel: LogLevel = LogLevel[MCP_LOG_LEVEL.toUpperCase() as keyof typeof LogLevel] || LogLevel.INFO;

/**
 * Internal logging function that handles log level filtering and formatting.
 * @param level The LogLevel of the message.
 * @param message The primary log message.
 * @param args Additional arguments to pass to the console method (e.g., objects, stack traces).
 */
const log = (level: LogLevel, message: string, ...args: any[]) => {
  if (level >= currentLogLevel) {
    const timestamp = new Date().toISOString();
    const levelName = LogLevel[level]; // Converts enum value (number) back to string name
    const formattedMessage = `[${timestamp}] [${levelName}] ${message}`;

    // Use appropriate console method based on log level
    switch (level) {
      case LogLevel.DEBUG:
        console.debug(formattedMessage, ...args);
        break;
      case LogLevel.INFO:
        console.info(formattedMessage, ...args);
        break;
      case LogLevel.WARN:
        console.warn(formattedMessage, ...args);
        break;
      case LogLevel.ERROR:
        console.error(formattedMessage, ...args);
        break;
      default:
        // Fallback for any unhandled log levels, though with a const enum, this is unlikely.
        console.log(formattedMessage, ...args);
        break;
    }
  }
};

/**
 * Public logger interface with methods for each log level.
 * These methods delegate to the internal `log` function.
 */
export const logger = {
  debug: (message: string, ...args: any[]) => log(LogLevel.DEBUG, message, ...args),
  info: (message: string, ...args: any[]) => log(LogLevel.INFO, message, ...args),
  warn: (message: string, ...args: any[]) => log(LogLevel.WARN, message, ...args),
  error: (message: string, ...args: any[]) => log(LogLevel.ERROR, message, ...args),
};

/**
 * Express middleware for logging incoming requests.
 * Logs the HTTP method, original URL, and IP address of the requester at INFO level.
 * @param req The Express request object.
 * @param res The Express response object.
 * @param next The next middleware function.
 */
export const requestLogger = (req: Request, res: Response, next: NextFunction) => {
  logger.info(`${req.method} ${req.originalUrl} from ${req.ip}`);
  next();
};