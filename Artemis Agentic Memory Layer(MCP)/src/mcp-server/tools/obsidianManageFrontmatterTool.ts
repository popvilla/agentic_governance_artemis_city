import { manageFrontmatter as manageObsidianFrontmatter } from '../../services/obsidianRestAPI/methods';
import { logger } from '../../utils/logger';

export async function manageFrontmatter(path: string, key: string, value: any) {
  try {
    logger.debug(`Managing frontmatter for note: ${path}, key: ${key}, value: ${value}`);
    await manageObsidianFrontmatter(path, key, value);
    logger.info(`Successfully updated frontmatter for note '${path}': key '${key}' set to '${value}'.`);
    return { success: true, message: `Frontmatter for '${path}' updated.` };
  } catch (error: any) {
    logger.error(`Error managing frontmatter for note '${path}': ${error.message}`);
    return { success: false, error: error.message };
  }
}
