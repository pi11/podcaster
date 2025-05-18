"""
Podcast Category Processor
This script processes and adds categories for podcasts stored in the database.
"""

import logging
import asyncio

# App specific imports
from app.models import Podcast
from app.services import PodcastService
from app.utils.helpers import init_db, close_db


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("youtube_downloader.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


async def main() -> None:
    await init_db()
    podcasts = await Podcast.filter(is_active=True)
    logger.info(f"Processing categories for {len(podcasts)} active podcasts")
    for podcast in podcasts:
        source = await podcast.source
        channel_id = await source.tg_channel
        print(channel_id.tg_id)
        await PodcastService.add_categories(id=podcast.id)
        print(f"{podcast.name} cats processed!")

    await close_db()


if __name__ == "__main__":
    logger.info("Finding categories")

    asyncio.run(main())

    logger.info("All files proccessed")
