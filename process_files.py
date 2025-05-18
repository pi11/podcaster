"""
YouTube Channel to MP3 Downloader Script for Podcast Manager
This script fetches videos from YouTube channels stored in the database,
converts them to MP3 format, and updates the database with the new podcasts.
"""

import os
import logging
import asyncio
import subprocess
from tortoise import Tortoise
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
from mutagen.id3 import TIT2, TALB  # Optional: Title, Album
from typing import Literal
from PIL import Image

# App specific imports
from app.models import Podcast

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("youtube_downloader.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Configuration
BASE_DIR = os.getcwd()
OUTPUT_DIR = os.path.join(BASE_DIR, os.getenv("MEDIA_DIR", "media"))

MAX_AUDIO_SIZE = 50 * 1000 * 1000  # about 50 Mb


async def init_db():
    """Initialize database connection"""
    logger.info("Initializing database connection")

    # Import your database configuration
    from app.config import TORTOISE_ORM

    await Tortoise.init(config=TORTOISE_ORM)
    logger.info("Database connection established")


async def close_db():
    """Close database connection"""
    logger.info("Closing database connection")
    await Tortoise.close_connections()


async def compress_podcast(
    podcast: Podcast,
    bitrate: Literal["64k", "32k", "16k"] = "64k",
    codec_format: Literal["libmp3lame", "libopus"] = "libmp3lame",
) -> bool:
    """
    Compress big file podcast

    Args:
        podcast: Podcast instance
        bitrate: Audio bitrate ("64k", "32k", "16k")
        codec_format: Audio codec format ("libmp3lame", "libopus")

    Returns:
        Dict with file path and size if successful, False otherwise
    """

    input_path = podcast.file
    if codec_format == "libmp3lame":
        ext = "mp3"
    else:
        ext = "opus"
    output_path = f"{podcast.file}-conv.{ext}"

    # first we try MP3, so we can embed Cover
    command = [
        "ffmpeg",
        "-i",
        input_path,
        "-y",
        "-q:a",
        "4",
        "-ac",
        "2",  # Ensure stereo
        "-c:a",
        codec_format,  # Use Opus codec
        "-b:a",
        bitrate,  # Set target bitrate
        output_path,
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Compressed file saved to: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error compressing file: {e}")
        return False

    new_size = os.path.getsize(output_path)
    if new_size < MAX_AUDIO_SIZE:
        print(f"Compressed from {podcast.filesize} to {new_size} (keep mp3)")
        return {"file": output_path, "size": new_size}

    print(f"Compressed size is too big: {new_size}, lets try another params")
    if codec_format == "libmp3lame":
        if bitrate == "64k":
            bitrate = "32k"
        else:
            codec_format = "libopus"
    else:
        if bitrate == "64k":
            bitrate = "32k"
        elif bitrate == "32k":
            bitrate = "16k"  # minimum bitrate =(
        else:  # can't do anything
            return False

    print(
        f"Trying to compress with new options: codec: {codec_format}, bitrate: {bitrate}"
    )

    return await compress_podcast(podcast, bitrate=bitrate, codec_format=codec_format)


async def embed_metadata(podcast):
    """
    Embed metadata to podcast:

    Args:
        podcast: Podcast instance

    Returns:
        bool: True if successful
    """

    # Paths
    path = podcast.file
    image_path = podcast.thumbnail

    # if path.endswith(".mp3"): # good its mp3 file

    audio = MP3(path, ID3=ID3)

    # If it doesn't have ID3 tag, add it
    try:
        audio.add_tags()
    except error:
        pass

    # convert webp to jpg
    img = Image.open(image_path)
    img.convert("RGB").save(image_path, "JPEG")

    # Embed the image
    with open(image_path, "rb") as albumart:
        audio.tags.add(
            APIC(
                encoding=3,  # 3 is for UTF-8
                mime="image/jpeg",  # or image/png
                type=3,  # 3 is for the cover (front) image
                desc="Cover",
                data=albumart.read(),
            )
        )

    # Optional: Add title, artist, album metadata
    audio.tags.add(TIT2(encoding=3, text=podcast.name))
    # audio.tags.add(TALB(encoding=3, text=podcast.source.name))

    # Save changes
    audio.save()
    print("Embedded album art successfully!")
    return True


async def main() -> None:
    await init_db()
    podcasts = await Podcast.filter(
        is_active=True, is_posted=False, is_processed=False, is_downloaded=True
    )

    for podcast in podcasts:

        # first lets process categories
        await PodcastService.add_categories(id=podcast.id)

        if podcast.filesize > MAX_AUDIO_SIZE:
            result = await compress_podcast(podcast)
            if result:
                print("Podcast compressed")
                podcast.file = result["file"]
                podcast.filesize = result["size"]
                await podcast.save()

        await embed_metadata(podcast)
        podcast.is_processed = True
        await podcast.save()
        print(f"{podcast.name} metadata embeded!")

    await close_db()


if __name__ == "__main__":
    logger.info("Starting MP3 processor")

    asyncio.run(main())

    logger.info("All files proccessed")
