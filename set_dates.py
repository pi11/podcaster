"""
Podcast Category Processor
This script processes and adds categories for podcasts stored in the database.
"""

import logging
import asyncio
from datetime import datetime

# App specific imports
from app.models import Podcast
from app.services import PodcastService
from app.utils.helpers import init_db, close_db
from tortoise.transactions import in_transaction
from tortoise.contrib.postgres.functions import Random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("youtube_downloader.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


async def main() -> None:
    await init_db()

    async with in_transaction():
        podcasts = await Podcast.filter(
            is_active=True, is_posted=False  # , is_downloaded=True
        )
        n = datetime.now()
        for podcast in podcasts:
            podcast.publication_date = n
            await podcast.save()
            # set currrent date

        podcasts = (
            await Podcast.filter(is_active=True, is_posted=False, is_downloaded=True)
            .annotate(order=Random())
            .order_by("order")
        )

        for podcast in podcasts:
            podcast.publication_date = await PodcastService.get_next_publication_date()
            await podcast.save()

    await close_db()


if __name__ == "__main__":
    logger.info("Finding categories")

    asyncio.run(main())

    logger.info("All files proccessed")
