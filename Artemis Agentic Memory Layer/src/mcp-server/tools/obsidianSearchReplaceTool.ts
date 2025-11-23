import { searchReplace as obsidianSearchReplace } from '../../services/obsidianRestAPI/methods';
import { logger } from '../../utils/logger';

export async function searchReplace(path: string, search: string, replace: string) {
  try {
    logger.debug(`Performing search and replace in note: ${path}, search: '${search}'`);
    const updatedContent = await obsidianSearchReplace(path, search, replace);
    logger.info(`Successfully performed search and replace in note: ${path}`);
    return { success: true, data: { path, content: updatedContent }, message: `Search and replace in '${path}' successful.` };
  } catch (error: any) {
    logger.error(`Error during search and replace in note '${path}': ${error.message}`);
    return { success: false, error: error.message };
  }
}
