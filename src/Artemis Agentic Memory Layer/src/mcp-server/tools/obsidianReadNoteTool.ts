import { readNote as readObsidianNote } from '../../services/obsidianRestAPI/methods';
import { logger } from '../../utils/logger';

export async function getContext(path: string) {
  try {
    logger.debug(`Attempting to read note: ${path}`);
    const noteContent = await readObsidianNote(path);
    logger.info(`Successfully read note: ${path}`);
    return { success: true, data: { path, content: noteContent } };
  } catch (error: any) {
    logger.error(`Error reading note '${path}': ${error.message}`);
    return { success: false, error: error.message };
  }
}
