import { listNotes as listObsidianNotes } from '../../services/obsidianRestAPI/methods';
import { logger } from '../../utils/logger';

export async function listNotes() {
  try {
    logger.debug('Listing all notes in the vault.');
    const notes = await listObsidianNotes();
    logger.info(`Found ${notes.length} notes in the vault.`);
    return { success: true, data: notes };
  } catch (error: any) {
    logger.error(`Error listing notes: ${error.message}`);
    return { success: false, error: error.message };
  }
}
