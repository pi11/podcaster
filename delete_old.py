"""
Podcast File Cleanup Script
This script removes files for inactive podcasts and updates their download status.
"""

import os
import logging
import asyncio

# App specific imports
from app.models import Podcast
from app.utils.helpers import init_db, close_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("youtube_downloader.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


async def remove_podcast_files(podcast: Podcast) -> None:
    """Remove all files associated with a podcast."""
    file_extensions = ["", "-thumb.jpg", "-conv.mp3", "-conv.opus"]

    for ext in file_extensions:
        file_path = f"{podcast.file}{ext}"
        try:
            os.remove(file_path)
            logger.debug(f"Removed file: {file_path}")
        except FileNotFoundError:
            logger.debug(f"File not found (skipping): {file_path}")
        except Exception as e:
            logger.warning(f"Error removing file {file_path}: {e}")


async def main() -> None:
    """Main function to process inactive podcasts and remove their files."""
    await init_db()

    try:
        podcasts = await Podcast.filter(is_active=False, is_downloaded=True)
        logger.info(f"Found {len(podcasts)} inactive podcasts to process")

        for podcast in podcasts:
            await remove_podcast_files(podcast)

            # Update podcast status
            podcast.is_downloaded = False
            await podcast.save()

            logger.info(f"Processed podcast: {podcast.name}")

    except Exception as e:
        logger.error(f"Error processing podcasts: {e}")
        raise
    finally:
        await close_db()


if __name__ == "__main__":
    logger.info("Starting file cleanup process")
    asyncio.run(main())
    logger.info("File cleanup process completed")
