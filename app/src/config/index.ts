import { logger } from '../utils/logger';

interface Config {
  PORT: number;
  MCP_API_KEY: string;
  OBSIDIAN_BASE_URL: string;
  OBSIDIAN_API_KEY: string;
  MCP_LOG_LEVEL: 'debug' | 'info' | 'warn' | 'error';
}

const config: Config = {
  PORT: parseInt(process.env.PORT || '3000', 10),
  MCP_API_KEY: process.env.MCP_API_KEY || '',
  OBSIDIAN_BASE_URL: process.env.OBSIDIAN_BASE_URL || '',
  OBSIDIAN_API_KEY: process.env.OBSIDIAN_API_KEY || '',
  MCP_LOG_LEVEL: (process.env.MCP_LOG_LEVEL as Config['MCP_LOG_LEVEL']) || 'info',
};

// Validate essential configuration
if (!config.MCP_API_KEY) {
  logger.error('MCP_API_KEY is not set. Please configure it in your .env file.');
  process.exit(1);
}

if (!config.OBSIDIAN_BASE_URL) {
  logger.error('OBSIDIAN_BASE_URL is not set. Please configure it in your .env file.');
  process.exit(1);
}

if (!config.OBSIDIAN_API_KEY) {
  logger.error('OBSIDIAN_API_KEY is not set. Please configure it in your .env file.');
  process.exit(1);
}

export const { PORT, MCP_API_KEY, OBSIDIAN_BASE_URL, OBSIDIAN_API_KEY, MCP_LOG_LEVEL } = config;
