"""
CLI commands for the podcast management application
"""

import os
import asyncio
import logging
import subprocess
import json
import time
from typing import Optional, Literal
from pathlib import Path
from datetime import datetime, timedelta
from urllib.parse import urlparse

import click
import aiohttp
from PIL import Image
import mutagen
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error, TIT2, TALB
from tortoise.transactions import in_transaction
from tortoise.contrib.postgres.functions import Random
import yt_dlp

# Import your app modules
from app.models import Podcast, Source, TgChannel
from app.services import PodcastService, SourceService, BannedWordsService
from app.utils.helpers import init_db, close_db

# Configuration
BASE_DIR = os.getcwd()
OUTPUT_DIR = os.path.join(BASE_DIR, os.getenv("MEDIA_DIR", "media"))
MAX_AUDIO_SIZE = 50 * 1000 * 1000  # about 50 Mb
MAX_VIDEOS_PER_CHANNEL = 20
MAX_VIDEO_AGE_DAYS = 1400
DOWNLOAD_AUDIO_QUALITY = "64"


# Configure logging
def setup_logging(verbose: bool = False) -> logging.Logger:
    """Set up logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO

    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_dir / "podcast_cli.log"),
            logging.StreamHandler(),
        ],
    )
    return logging.getLogger(__name__)


async def remove_podcast_files(podcast: Podcast, logger: logging.Logger) -> None:
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


@click.group()
@click.version_option()
def cli():
    """Podcast Management CLI Tools

    A collection of utilities for managing your podcast application.
    """
    pass


@cli.command()
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would be deleted without actually deleting files",
)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.option("--force", is_flag=True, help="Skip confirmation prompt")
def cleanup(dry_run: bool, verbose: bool, force: bool):
    """Clean up files for inactive podcasts.

    This command removes files associated with podcasts that are marked as
    inactive and updates their download status to False.
    """
    logger = setup_logging(verbose)

    async def _cleanup():
        await init_db()

        try:
            podcasts = await Podcast.filter(is_active=False, is_downloaded=True)

            if not podcasts:
                click.echo("✅ No inactive podcasts with downloaded files found.")
                return

            logger.info(f"Found {len(podcasts)} inactive podcasts to process")

            if dry_run:
                click.echo("🔍 DRY RUN - No files will be deleted")
                click.echo("Files that would be processed:")
                for podcast in podcasts:
                    click.echo(f"  • {podcast.name} ({podcast.file}*)")
                return

            if not force:
                click.echo(f"About to process {len(podcasts)} inactive podcasts:")
                for podcast in podcasts[:5]:  # Show first 5
                    click.echo(f"  • {podcast.name}")
                if len(podcasts) > 5:
                    click.echo(f"  ... and {len(podcasts) - 5} more")

                if not click.confirm("Continue with cleanup?"):
                    click.echo("❌ Cleanup cancelled.")
                    return

            processed_count = 0
            error_count = 0

            with click.progressbar(
                podcasts, label="Processing podcasts", show_eta=True
            ) as bar:
                for podcast in bar:
                    try:
                        await remove_podcast_files(podcast, logger)
                        podcast.is_downloaded = False
                        await podcast.save()
                        logger.info(f"Processed podcast: {podcast.name}")
                        processed_count += 1
                    except Exception as e:
                        logger.error(f"Error processing {podcast.name}: {e}")
                        error_count += 1

            # Summary
            click.echo(f"✅ Cleanup completed!")
            click.echo(f"   Processed: {processed_count}")
            if error_count > 0:
                click.echo(f"   Errors: {error_count}")

        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
            click.echo(f"❌ Error: {e}", err=True)
            raise
        finally:
            await close_db()

    asyncio.run(_cleanup())


@cli.command()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.option("--active-only", is_flag=True, help="Process only active podcasts")
def add_categories(verbose: bool, active_only: bool):
    """Add categories to podcasts using AI processing."""
    logger = setup_logging(verbose)

    async def _add_categories():
        await init_db()

        try:
            filters = {"is_active": True} if active_only else {}
            podcasts = await Podcast.filter(**filters)

            if not podcasts:
                click.echo("✅ No podcasts found to process.")
                return

            logger.info(f"Processing categories for {len(podcasts)} podcasts")

            processed_count = 0
            error_count = 0

            with click.progressbar(
                podcasts, label="Adding categories", show_eta=True
            ) as bar:
                for podcast in bar:
                    try:
                        source = await podcast.source
                        if hasattr(source, "tg_channel"):
                            channel_id = await source.tg_channel
                            if verbose:
                                click.echo(f"Processing channel ID: {channel_id.tg_id}")

                        await PodcastService.add_categories(id=podcast.id)

                        if verbose:
                            click.echo(f"✅ {podcast.name} categories processed!")

                        processed_count += 1

                    except Exception as e:
                        logger.error(f"Error processing {podcast.name}: {e}")
                        error_count += 1

            # Summary
            click.echo(f"✅ Category processing completed!")
            click.echo(f"   Processed: {processed_count}")
            if error_count > 0:
                click.echo(f"   Errors: {error_count}")

        except Exception as e:
            logger.error(f"Error during category processing: {e}")
            click.echo(f"❌ Error: {e}", err=True)
            raise
        finally:
            await close_db()

    asyncio.run(_add_categories())


@cli.command()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.option("--watch", "-w", is_flag=True, help="Run continuously every 20 seconds")
@click.option(
    "--compress/--no-compress",
    default=True,
    help="Enable or disable compression for large files",
)
def process_files(verbose: bool, watch: bool, compress: bool):
    """Process podcast files: compress large files and embed metadata."""
    logger = setup_logging(verbose)

    async def _process_files():
        await init_db()

        try:
            podcasts = await Podcast.filter(
                is_active=True, is_posted=False, is_processed=False, is_downloaded=True
            )

            if not podcasts:
                if verbose:
                    click.echo("✅ No podcasts found to process.")
                return

            logger.info(f"Processing {len(podcasts)} podcasts")

            processed_count = 0
            compressed_count = 0
            error_count = 0

            with click.progressbar(
                podcasts, label="Processing files", show_eta=True
            ) as bar:
                for podcast in bar:
                    try:
                        # Add categories first
                        await PodcastService.add_categories(id=podcast.id)

                        # Compress if needed and enabled
                        if compress and podcast.filesize > MAX_AUDIO_SIZE:
                            result = await compress_podcast(podcast)
                            if result:
                                click.echo(f"📦 Compressed: {podcast.name}")
                                podcast.file = result["file"]
                                podcast.filesize = result["size"]
                                podcast.bitrate = result["bitrate"]
                                podcast.is_processed = True
                                compressed_count += 1
                            else:
                                podcast.is_processed = True
                            await podcast.save()

                        # Embed metadata
                        await embed_metadata(podcast)

                        # Mark as processed
                        podcast.is_processed = True
                        await podcast.save()

                        if verbose:
                            click.echo(f"✅ {podcast.name} processed!")

                        processed_count += 1

                    except Exception as e:
                        logger.error(f"Error processing {podcast.name}: {e}")
                        error_count += 1

            # Summary
            if processed_count > 0:
                click.echo(f"✅ File processing completed!")
                click.echo(f"   Processed: {processed_count}")
                click.echo(f"   Compressed: {compressed_count}")
                if error_count > 0:
                    click.echo(f"   Errors: {error_count}")

        except Exception as e:
            logger.error(f"Error during file processing: {e}")
            click.echo(f"❌ Error: {e}", err=True)
            raise
        finally:
            await close_db()

    if watch:
        click.echo("👀 Starting continuous processing (Ctrl+C to stop)")
        try:
            while True:
                asyncio.run(_process_files())
                time.sleep(20)
        except KeyboardInterrupt:
            click.echo("\n⏹️  Processing stopped by user.")
    else:
        asyncio.run(_process_files())


@cli.command("download")
@click.option("--source-id", type=int, help="Download from specific source ID only")
@click.option("--url", help="Download from specific URL")
@click.option("--tg-channel", help="Telegram channel ID for URL downloads")
@click.option("--quality", default="64", help="Audio quality in kbps")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.option(
    "--dry-run", is_flag=True, help="Show what would be downloaded without downloading"
)
def download_youtube(
    source_id: Optional[int],
    url: Optional[str],
    tg_channel: Optional[str],
    quality: str,
    verbose: bool,
    dry_run: bool,
):
    """Download videos from YouTube channels as MP3."""
    logger = setup_logging(verbose)

    # Check if yt-dlp is installed
    try:
        subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        click.echo(
            "❌ yt-dlp is not installed. Install with: pip install yt-dlp", err=True
        )
        return

    async def _download():
        await init_db()

        try:
            # Handle single URL download
            if url:
                if dry_run:
                    click.echo(f"🔍 Would download from URL: {url}")
                    return

                # Get tg_channel object if provided
                tg_channel_obj = None
                if tg_channel:
                    tg_channel_obj = await TgChannel.filter(id=tg_channel).first()
                    if not tg_channel_obj:
                        click.echo(
                            f"❌ Telegram channel with ID {tg_channel} not found."
                        )
                        return

                # Ensure output directory exists
                os.makedirs(OUTPUT_DIR, exist_ok=True)

                downloaded = await download_single_url(
                    url, tg_channel_obj, quality, verbose, logger
                )
                if downloaded:
                    click.echo(f"✅ Downloaded: {downloaded['title']}")
                else:
                    click.echo("❌ Failed to download from URL")
                return

            # Get sources
            if source_id:
                sources = await Source.filter(id=source_id)
                if not sources:
                    click.echo(f"❌ Source with ID {source_id} not found.")
                    return
            else:
                sources = await SourceService.get_all()

            if not sources:
                click.echo("❌ No sources found.")
                return

            # Ensure output directory exists
            os.makedirs(OUTPUT_DIR, exist_ok=True)

            logger.info(f"Found {len(sources)} sources to process")

            total_downloaded = 0

            for source in sources:
                try:
                    if dry_run:
                        click.echo(f"🔍 Would process: {source.name} ({source.url})")
                        continue

                    click.echo(f"📺 Processing: {source.name}")
                    downloaded_count = await process_channel_download(
                        source, source.max_videos_per_channel, quality, verbose, logger
                    )
                    total_downloaded += downloaded_count

                    if verbose:
                        click.echo(
                            f"✅ Downloaded {downloaded_count} from {source.name}"
                        )

                except Exception as e:
                    logger.error(f"Error processing source {source.name}: {e}")
                    click.echo(f"❌ Error processing {source.name}: {e}")

            if not dry_run:
                click.echo(
                    f"✅ Download completed! Total downloaded: {total_downloaded}"
                )

        except Exception as e:
            logger.error(f"Error during download: {e}")
            click.echo(f"❌ Error: {e}", err=True)
            raise
        finally:
            await close_db()

    asyncio.run(_download())


# Helper functions for the new commands


async def compress_podcast(
    podcast: Podcast,
    bitrate: Literal["96k", "64k"] = "96k",
) -> bool:
    """Compress big file podcast."""
    input_path = podcast.file
    output_path = f"{podcast.file}-conv.mp3"

    command = [
        "ffmpeg",
        "-i",
        input_path,
        "-y",
        "-ac",
        "2",
        "-b:a",
        bitrate,
        output_path,
    ]

    try:
        subprocess.run(command, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        return False

    new_size = os.path.getsize(output_path)
    if new_size < MAX_AUDIO_SIZE:
        return {"file": output_path, "size": new_size, "bitrate": bitrate}

    # Try different compression settings

    if bitrate == "96k":
        bitrate = "64k"
    elif bitrate == "64k":  # Min quality
        print("64k")
        return {"file": output_path, "size": new_size, "bitrate": bitrate}

    return await compress_podcast(podcast, bitrate=bitrate)


async def embed_metadata(podcast):
    """Embed metadata to podcast."""
    path = podcast.file
    image_path = podcast.thumbnail

    try:
        audio = MP3(path, ID3=ID3)
    except mutagen.mp3.HeaderNotFoundError:
        return

    try:
        audio.add_tags()
    except error:
        pass

    # Convert webp to jpg if needed
    try:
        img = Image.open(image_path)
        img.convert("RGB").save(image_path, "JPEG")

        # Embed the image
        with open(image_path, "rb") as albumart:
            audio.tags.add(
                APIC(
                    encoding=3,
                    mime="image/jpeg",
                    type=3,
                    desc="Cover",
                    data=albumart.read(),
                )
            )

        # Add title metadata
        audio.tags.add(TIT2(encoding=3, text=podcast.name))
        audio.save()
        return True
    except Exception as e:
        logging.getLogger(__name__).warning(f"Error embedding metadata: {e}")
        return False


async def process_channel_download(
    source, max_videos: int, quality: str, verbose: bool, logger
) -> int:
    """Process a YouTube channel for downloads."""
    try:
        channel_dir = os.path.join(
            OUTPUT_DIR, str(source.id) + "_" + source.name.replace(" ", "_")
        )

        banned_words = await BannedWordsService.get_all()

        # Get channel videos
        cmd = [
            "yt-dlp",
            # "--cookies-from-browser",
            # "firefox",
            "--dump-json",
            "--flat-playlist",
            "--playlist-end",
            str(max_videos),
            source.url,
        ]
        process = subprocess.run(cmd, capture_output=True, text=True, check=True)
        videos = [
            json.loads(line) for line in process.stdout.splitlines() if line.strip()
        ]

        downloaded_count = 0
        print("Processing videos...")
        for video in videos:
            # Check if already exists
            podcast = await Podcast.filter(yt_id=video["id"]).first()
            if podcast:
                print(f"Podcast already downloaded: {podcast}, skipping")
                continue
            video_url = f"https://www.youtube.com/watch?v={video['id']}"
            print(f"Video url: {video_url}")
            # Get video info
            video_info = get_video_info(video_url)
            if not video_info or "error" in video_info:
                continue

            duration = video_info.get("duration", 0)
            if duration < source.min_duration or duration > source.max_duration:
                continue

            # Check banned words
            title_lower = video_info["title"].lower()
            if any(bn.name.lower() in title_lower for bn in banned_words):
                continue

            if not podcast:
                nd = await PodcastService.get_next_publication_date()
                podcast_data = {
                    "name": video_info.get("title"),
                    "description": video_info.get("description", ""),
                    "url": video_url,
                    "source_id": source.id,
                    "tg_channel_id": source.tg_channel_id,
                    "yt_id": video_info.get("id"),
                    "publication_date": nd,
                    "is_processed": False,
                    "file": None,
                    "duration": video_info.get("duration"),
                    "is_posted": False,
                    "thumbnail_url": video_info.get("thumbnail", ""),
                }
                logger.info("New podcast:")
                logger.info(podcast_data)

                podcast = await PodcastService.create(podcast_data)
            elif podcast.is_downloaded:
                continue

            if not podcast.is_active:
                logger.info(f"Podcast is inactive, skipping download: {podcast.name}")
                continue

            # Check theme if needed
            if source.only_related:
                if not await PodcastService.check_theme(id=podcast.id):
                    continue

            if podcast.is_active:
                # Download
                logger.info(f"Downloading new audio: {video_url}: {podcast.name}")
                downloaded = download_audio(video_url, channel_dir, quality)
            else:
                downloaded = False
                logger.info(f"Not downloading - {podcast.name}")
            if downloaded:
                # Download thumbnail
                thumbnail_path = f"{downloaded.get('file_path')}-thumb.jpg"
                async with aiohttp.ClientSession() as session:
                    async with session.get(podcast.thumbnail_url) as response:
                        if response.status == 200:
                            with open(thumbnail_path, "wb") as f:
                                f.write(await response.read())

                # Update podcast
                filesize = os.path.getsize(downloaded.get("file_path", ""))
                podcast.file = downloaded.get("file_path")
                podcast.filesize = filesize
                podcast.thumbnail = thumbnail_path
                podcast.is_downloaded = True
                await podcast.save()

                downloaded_count += 1

                if verbose:
                    click.echo(f"  ✅ Downloaded: {video_info.get('title')}")

        return downloaded_count

    except Exception as e:

        logger.error(f"Error processing channel {source.name}: {e}")
        import traceback

        print(traceback.format_exc())
        return 0


def get_video_info(url):
    """Get video information using yt-dlp."""
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        # "cookiesfrombrowser": ("firefox",),
        # "cookies_from_browser": "firefox",
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get("title"),
                "duration": info.get("duration"),
                "upload_date": info.get("upload_date"),
                "uploader": info.get("uploader"),
                "view_count": info.get("view_count"),
                "description": info.get("description"),
                "thumbnail": info.get("thumbnail"),
                "id": info.get("id"),
            }
    except Exception as e:
        return {"error": str(e)}


def download_audio(video_url, output_path, quality="64"):
    """Download YouTube video as MP3."""
    try:
        os.makedirs(output_path, exist_ok=True)

        # Get video info first
        info_cmd = [
            "yt-dlp",
            "--dump-json",
            # "--cookies-from-browser",
            # "firefox",
            "--no-playlist",
            video_url,
        ]
        info_process = subprocess.run(
            info_cmd, capture_output=True, text=True, check=True
        )
        video_info = json.loads(info_process.stdout)

        # Extract upload date
        upload_date_str = video_info.get("upload_date", "")
        if upload_date_str:
            try:
                upload_date = datetime.strptime(upload_date_str, "%Y%m%d")
            except ValueError:
                upload_date = datetime.now()
        else:
            upload_date = datetime.now()

        # Download command
        output_template = os.path.join(output_path, "%(id)s.%(ext)s")
        cmd = [
            "yt-dlp",
            "-f",
            "bestaudio",
            "--extract-audio",
            "--audio-format",
            "mp3",
            "--audio-quality",
            quality,
            "--embed-thumbnail",
            "--add-metadata",
            "--no-playlist",
            # "--cookies-from-browser",
            # "firefox",
            "-o",
            output_template,
            video_url,
        ]

        print("Downloading")
        subprocess.run(cmd, capture_output=True, text=True, check=True)

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

        return None

    except Exception:
        return None


async def download_single_url(
    url: str, tg_channel_obj, quality: str, verbose: bool, logger
) -> dict:
    """Download a single URL and create podcast entry."""
    try:
        # Get video info
        video_info = get_video_info(url)
        if not video_info or "error" in video_info:
            logger.error(f"Failed to get video info for {url}")
            return None

        # Check if podcast already exists
        existing_podcast = await Podcast.filter(url=url).first()
        if existing_podcast:
            logger.info(f"Podcast already exists: {existing_podcast.name}")
            return {"title": existing_podcast.name}

        # Create directory for download
        download_dir = os.path.join(OUTPUT_DIR, "single_downloads")

        # Download the audio
        logger.info(f"Downloading: {video_info.get('title')}")
        downloaded = download_audio(url, download_dir, quality)

        if not downloaded:
            logger.error(f"Failed to download {url}")
            return None

        # Get next publication date
        nd = await PodcastService.get_next_publication_date()

        # Create podcast entry
        podcast_data = {
            "name": video_info.get("title"),
            "description": video_info.get("description", ""),
            "url": url,
            "source_id": None,  # Source should be null as requested
            "tg_channel_id": tg_channel_obj.id if tg_channel_obj else None,
            "yt_id": video_info.get("id"),
            "publication_date": nd,
            "is_processed": False,
            "file": downloaded.get("file_path"),
            "filesize": os.path.getsize(downloaded.get("file_path", "")),
            "duration": video_info.get("duration"),
            "is_posted": False,
            "is_downloaded": True,
            "thumbnail_url": video_info.get("thumbnail", ""),
        }

        podcast = await PodcastService.create(podcast_data)

        # Download thumbnail
        if video_info.get("thumbnail"):
            thumbnail_path = f"{downloaded.get('file_path')}-thumb.jpg"
            async with aiohttp.ClientSession() as session:
                async with session.get(video_info.get("thumbnail")) as response:
                    if response.status == 200:
                        with open(thumbnail_path, "wb") as f:
                            f.write(await response.read())

                        # Update podcast with thumbnail path
                        podcast.thumbnail = thumbnail_path
                        await podcast.save()

        logger.info(f"Created podcast: {podcast.name}")

        if verbose:
            click.echo(f"  📁 File: {downloaded.get('file_path')}")
            click.echo(f"  📊 Size: {podcast.filesize / 1000 / 1000:.2f} MB")
            click.echo(f"  ⏱️  Duration: {video_info.get('duration')} seconds")

        return {"title": podcast.name, "id": podcast.id}

    except Exception as e:
        logger.error(f"Error downloading single URL {url}: {e}")
        return None


if __name__ == "__main__":
    cli()
