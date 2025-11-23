import { manageTags as manageObsidianTags } from '../../services/obsidianRestAPI/methods';
import { logger } from '../../utils/logger';

export async function manageTags(path: string, tags: string[], action: 'add' | 'remove') {
  try {
    logger.debug(`Managing tags for note: ${path}, action: ${action}, tags: ${tags.join(', ')}`);
    await manageObsidianTags(path, tags, action);
    logger.info(`Successfully ${action}ed tags for note '${path}': ${tags.join(', ')}.`);
    return { success: true, message: `Tags for '${path}' ${action}ed successfully.` };
  } catch (error: any) {
    logger.error(`Error managing tags for note '${path}': ${error.message}`);
    return { success: false, error: error.message };
  }
}
