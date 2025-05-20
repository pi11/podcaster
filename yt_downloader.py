"""
YouTube Channel to MP3 Downloader Script for Podcast Manager
This script fetches videos from YouTube channels stored in the database,
converts them to MP3 format, and updates the database with the new podcasts.
"""

import os
import logging
import aiohttp
import asyncio
import datetime
from datetime import timedelta
from urllib.parse import urlparse
import subprocess
import json
from tortoise import Tortoise
import yt_dlp

# App specific imports
from app.models import Source, Podcast
from app.services import SourceService, PodcastService
from app.utils.helpers import close_db, init_db

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

MAX_VIDEOS_PER_CHANNEL = 10  # Maximum number of videos to download per channel
MAX_VIDEO_AGE_DAYS = 1400  # Only download videos published within the last 14 days
DOWNLOAD_AUDIO_QUALITY = "64"  # Audio quality in kbps


def download_audio(video_url, output_path):
    """
    Download a YouTube video as MP3 using yt-dlp

    Args:
        video_url: YouTube video URL
        output_path: Directory to save the MP3 file

    Returns:
        Dictionary with download information or None if failed
    """
    try:
        # Ensure output directory exists
        os.makedirs(output_path, exist_ok=True)

        # Prepare yt-dlp command
        output_template = os.path.join(output_path, "%(id)s.%(ext)s")

        # First, get video info including upload date
        info_cmd = ["yt-dlp", "--dump-json", "--no-playlist", video_url]

        # Run the info command and capture output
        info_process = subprocess.run(
            info_cmd, capture_output=True, text=True, check=True
        )

        # Parse the JSON output
        video_info = json.loads(info_process.stdout)

        # Extract upload date
        upload_date_str = video_info.get("upload_date", "")

        # Convert YYYYMMDD format to datetime object
        if upload_date_str:
            try:
                upload_date = datetime.datetime.strptime(upload_date_str, "%Y%m%d")
            except ValueError:
                upload_date = datetime.datetime.now()
        else:
            upload_date = datetime.datetime.now()

        # Check if video is too old
        if (datetime.datetime.now() - upload_date) > timedelta(days=MAX_VIDEO_AGE_DAYS):
            logger.info(
                f"Skipping video {video_info.get('title')} - too old ({upload_date.strftime('%Y-%m-%d')})"
            )
            return None

        # Download command
        cmd = [
            "yt-dlp",
            "-f",
            "bestaudio",
            "--extract-audio",
            "--audio-format",
            "mp3",
            "--audio-quality",
            DOWNLOAD_AUDIO_QUALITY,
            "--embed-thumbnail",
            "--add-metadata",
            "--no-playlist",
            "-o",
            output_template,
            video_url,
        ]

        # Execute the download command
        logger.info(f"Downloading: {video_info.get('title')}")
        process = subprocess.run(cmd, capture_output=True, text=True, check=True)

        # Check for output file
        expected_filename = f"{video_info.get('id')}.mp3"
        expected_path = os.path.join(output_path, expected_filename)

        if os.path.exists(expected_path):
            return {
                "title": video_info.get("title"),
                "id": video_info.get("id"),
                "url": video_url,
                "upload_date": upload_date,
                "filename": expected_filename,
                "file_path": expected_path,
                "thumbnail": video_info["thumbnail"],
                "channel": video_info.get("channel", ""),
                "duration": video_info.get("duration", 0),
            }
        else:
            logger.error(f"Download succeeded but file not found: {expected_path}")
            logger.debug(f"Command output: {process.stdout}")
            return None

    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to download {video_url}: {e}")
        logger.debug(f"Error details: stdout={e.stdout}, stderr={e.stderr}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error downloading {video_url}: {e}")
        return None


async def process_channel(source):
    """
    Process a YouTube channel to download videos as MP3

    Args:
        source: Source object with YouTube channel information
    """

    def get_video_info(url):
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                # Extract relevant information
                video_info = {
                    "title": info.get("title"),
                    "duration": info.get("duration"),  # in seconds
                    "upload_date": info.get("upload_date"),
                    "uploader": info.get("uploader"),
                    "view_count": info.get("view_count"),
                    "like_count": info.get("like_count"),
                    "description": info.get("description"),
                    "thumbnail": info.get("thumbnail"),
                    "formats": len(info.get("formats", [])),
                    "id": info.get("id"),
                }
                # print(video_info)

                return video_info
        except Exception as e:
            print("Error extracting video info")
            return {"error": str(e)}

    try:
        logger.info(f"Processing channel: {source.name} ({source.url})")

        # Extract channel ID or username from source URL
        parsed_url = urlparse(source.url)

        # Create folder for this channel
        channel_dir = os.path.join(
            OUTPUT_DIR, str(source.id) + "_" + source.name.replace(" ", "_")
        )

        # Get channel videos list
        cmd = [
            "yt-dlp",
            "--dump-json",
            "--flat-playlist",
            "--playlist-end",
            str(source.max_videos_per_channel),
            source.url,
        ]

        try:
            process = subprocess.run(cmd, capture_output=True, text=True, check=True)

            # Process each video in the playlist
            videos = [
                json.loads(line) for line in process.stdout.splitlines() if line.strip()
            ]
            logger.info(f"Found {len(videos)} videos from {source.name}")

            for video in videos:
                video_url = f"https://www.youtube.com/watch?v={video['id']}"
                video_info = get_video_info(video_url)

                logger.info(f"Processing video: {video_url}")
                duration = video_info.get("duration")
                if duration < source.min_duration:
                    logger.info(f"Video duration {duration} < min duration for channel")
                    continue
                if duration > source.max_duration:
                    logger.info(f"Video duration {duration} > max duration for channel")
                    continue

                # Check if this video already exists in our database
                podcast = await Podcast.filter(yt_id=video["id"]).first()
                if podcast:
                    logger.info(f"Video already in database: {video['title']}")

                    if podcast.is_downloaded:
                        logger.info(f"and downloaded...")
                        continue
                    if not podcast.is_active:
                        logger.info(f"Podcast deactivated")
                        continue

                else:
                    nd = await PodcastService.get_next_publication_date()
                    podcast_data = {
                        "name": video_info.get("title"),
                        "description": video_info.get("description", ""),
                        "url": video_url,
                        "source_id": source.id,
                        "yt_id": video_info.get("id"),
                        "publication_date": nd,
                        "is_processed": False,
                        "file": None,
                        "is_posted": False,  # Set to False by default, can be activated later
                        "thumbnail_url": video_info.get("thumbnail", ""),
                    }
                    podcast = await PodcastService.create(podcast_data)

                if source.only_related:
                    # check if video related to one of the categories
                    logger.info("Check if podcast related to themes")
                    good = await PodcastService.check_theme(id=podcast.id)
                else:
                    good = True

                if good:
                    # Download the video as MP3
                    downloaded = download_audio(video_url, channel_dir)
                else:
                    downloaded = False

                if downloaded:
                    logger.info(f"File downloaded: {downloaded['file_path']}")
                    filesize = os.path.getsize(downloaded.get("file_path", 0))

                    thumbnail_path = f"{downloaded.get("file_path")}-thumb.jpg"
                    async with aiohttp.ClientSession() as session:
                        async with session.get(podcast.thumbnail_url) as response:
                            if response.status == 200:
                                with open(thumbnail_path, "wb") as f:
                                    f.write(await response.read())
                    # Update podcast entry in database
                    podcast.file = downloaded.get("file_path")
                    podcast.filesize = filesize
                    podcast.thumbnail = thumbnail_path
                    podcast.is_downloaded = True
                    await podcast.save()
                else:
                    logger.error(f"Download failed or skiped")

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to get videos from {source.name}: {e}")
            logger.debug(f"Error details: stdout={e.stdout}, stderr={e.stderr}")

    except Exception as e:
        logger.error(f"Unexpected error processing channel {source.name}: {e}")


async def main():
    """Main function to process all sources and download videos"""
    try:
        # Initialize the database
        await init_db()

        # Ensure output directory exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # Get all sources from database
        sources = await SourceService.get_all()

        if not sources:
            logger.warning("No sources found in database")
            return

        logger.info(f"Found {len(sources)} sources to process")

        # Process each source
        for source in sources:
            await process_channel(source)

        logger.info("All channels processed successfully")

    except Exception as e:
        logger.error(f"Unexpected error in main function: {e}")
    finally:
        # Close database connection
        await close_db()


if __name__ == "__main__":
    logger.info("Starting YouTube to MP3 downloader")

    # Check if yt-dlp is installed
    try:
        subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error(
            "yt-dlp is not installed or not in PATH. Please install it with: pip install yt-dlp"
        )
        exit(1)

    # Run the main async function
    asyncio.run(main())

    logger.info("Download process completed")
