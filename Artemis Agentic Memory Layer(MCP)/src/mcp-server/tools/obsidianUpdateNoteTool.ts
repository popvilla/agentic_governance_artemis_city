import { updateNote as updateObsidianNote } from '../../services/obsidianRestAPI/methods';
import { logger } from '../../utils/logger';

export async function appendContext(path: string, content: string) {
  try {
    logger.debug(`Attempting to append context to note: ${path}`);
    await updateObsidianNote(path, content, { append: true });
    logger.info(`Successfully appended context to note: ${path}`);
    return { success: true, message: `Content appended to note '${path}'.` };
  } catch (error: any) {
    logger.error(`Error appending context to note '${path}': ${error.message}`);
    return { success: false, error: error.message };
  }
}

export async function updateNote(path: string, content: string) {
  try {
    logger.debug(`Attempting to update note: ${path}`);
    await updateObsidianNote(path, content, { append: false });
    logger.info(`Successfully updated note: ${path}`);
    return { success: true, message: `Note '${path}' updated.` };
  } catch (error: any) {
    logger.error(`Error updating note '${path}': ${error.message}`);
    return { success: false, error: error.message };
  }
}
