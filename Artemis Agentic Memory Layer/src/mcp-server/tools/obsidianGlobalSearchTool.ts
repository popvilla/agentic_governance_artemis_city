import { searchNotes as searchObsidianNotes } from '../../services/obsidianRestAPI/methods';
import { logger } from '../../utils/logger';

export async function searchNotes(query: string) {
  try {
    logger.debug(`Performing global search for query: ${query}`);
    const searchResults = await searchObsidianNotes(query);
    logger.info(`Found ${searchResults.length} results for query: ${query}`);
    return { success: true, data: searchResults };
  } catch (error: any) {
    logger.error(`Error during global search for query '${query}': ${error.message}`);
    return { success: false, error: error.message };
  }
}
