import { deleteNote as deleteObsidianNote } from '../../services/obsidianRestAPI/methods';
import { logger } from '../../utils/logger';

export async function deleteNote(path: string) {
  try {
    logger.debug(`Attempting to delete note: ${path}`);
    await deleteObsidianNote(path);
    logger.info(`Successfully deleted note: ${path}`);
    return { success: true, message: `Note '${path}' deleted successfully.` };
  } catch (error: any) {
    logger.error(`Error deleting note '${path}': ${error.message}`);
    return { success: false, error: error.message };
  }
}
