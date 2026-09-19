"""
CLI commands for the podcast management application
"""

import os
import asyncio
import logging
import subprocess
import json
import time
import traceback
import random
import re
import urllib.request

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
import yt_dlp

# Import your app modules
from app.models import Podcast, Source, TgChannel
from app.services import PodcastService, SourceService, BannedWordsService, ProxyService
from app.utils.helpers import init_db, close_db

# Configuration
BASE_DIR = os.getcwd()
OUTPUT_DIR = os.path.join(BASE_DIR, os.getenv("MEDIA_DIR", "media"))
MAX_AUDIO_SIZE = 50 * 1000 * 1000  # about 50 Mb
MAX_VIDEOS_PER_CHANNEL = 20
MAX_VIDEO_AGE_DAYS = 1400
DOWNLOAD_AUDIO_QUALITY = "64"
POT_PROVIDER_URL = os.getenv("POT_PROVIDER_URL", "http://127.0.0.1:4416")
YOUTUBE_PLAYER_CLIENT = "tv_simply"
YOUTUBE_FALLBACK_CLIENTS = tuple(
    client.strip()
    for client in os.getenv(
        "YOUTUBE_FALLBACK_CLIENTS", "mweb,android_vr,web_safari"
    ).split(",")
    if client.strip()
)


class DownloadCommandError(RuntimeError):
    """A failed yt-dlp subprocess with output retained for retry decisions."""

    def __init__(self, stage: str, returncode: int, stderr: str):
        super().__init__(f"{stage} failed with return code {returncode}")
        self.stage = stage
        self.returncode = returncode
        self.stderr = stderr


class MembersOnlyVideoError(RuntimeError):
    """A video cannot be downloaded without a channel membership."""


def redact_proxy(proxy: Optional[str]) -> str:
    """Return a log-safe proxy URL without its password."""
    if not proxy:
        return "direct connection"
    parsed = urlparse(proxy)
    host = parsed.hostname or "unknown-host"
    port = f":{parsed.port}" if parsed.port else ""
    username = f"{parsed.username}:***@" if parsed.username else ""
    return f"{parsed.scheme}://{username}{host}{port}"


def redact_po_tokens(value: str) -> str:
    """Remove short-lived YouTube PO tokens from verbose yt-dlp output."""
    value = re.sub(
        r"(?i)(Generated POT:\s*)\S+", r"\1***REDACTED***", value
    )
    value = re.sub(
        r"(?i)(po_token=')([^']+)", r"\1***REDACTED***", value
    )
    return re.sub(
        r"(?i)([?&]pot=)[^&\s]+", r"\1***REDACTED***", value
    )


def is_valid_proxy(proxy: str) -> bool:
    try:
        parsed = urlparse(proxy)
        return (
            parsed.scheme in {"http", "https"}
            and parsed.hostname is not None
            and parsed.port is not None
        )
    except ValueError:
        return False


def add_proxy_argument(command: list[str], proxy: Optional[str]) -> list[str]:
    """Add yt-dlp's proxy argument only when a proxy is configured."""
    if proxy:
        command.extend(["--proxy", proxy])
    return command


def add_youtube_extractor_arguments(
    command: list[str], logger, player_client: str = YOUTUBE_PLAYER_CLIENT
) -> list[str]:
    """Configure automatic PO tokens for YouTube media requests."""
    command.extend(
        [
            "--impersonate",
            "chrome",
            "--remote-components",
            "ejs:github",
            "--extractor-args",
            f"youtube:player_client={player_client};pot_trace=true",
            "--extractor-args",
            f"youtubepot-bgutilhttp:base_url={POT_PROVIDER_URL}",
        ]
    )
    if logger.isEnabledFor(logging.DEBUG):
        command.append("--verbose")
    return command


def log_command(logger, stage: str, command: list[str], proxy: Optional[str]) -> None:
    safe_command = [redact_proxy(value) if value == proxy else value for value in command]
    logger.debug("%s command: %s", stage, " ".join(safe_command))
    logger.debug("%s network route: %s", stage, redact_proxy(proxy))


def run_download_command(command, logger, stage, proxy, check=True):
    """Run yt-dlp and record diagnostics useful for download failures."""
    log_command(logger, stage, command, proxy)
    started_at = time.monotonic()
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    elapsed = time.monotonic() - started_at
    logger.debug("%s finished: return_code=%s elapsed=%.2fs", stage, result.returncode, elapsed)
    safe_stdout = result.stdout.replace(proxy, redact_proxy(proxy)) if proxy else result.stdout
    safe_stderr = result.stderr.replace(proxy, redact_proxy(proxy)) if proxy else result.stderr
    safe_stdout = redact_po_tokens(safe_stdout)
    safe_stderr = redact_po_tokens(safe_stderr)
    if safe_stdout.strip():
        logger.debug("%s stdout:\n%s", stage, safe_stdout.strip())
    if safe_stderr.strip():
        log = logger.error if result.returncode else logger.debug
        log("%s stderr:\n%s", stage, safe_stderr.strip())
    if check and result.returncode:
        raise DownloadCommandError(stage, result.returncode, safe_stderr)
    return result


def check_pot_provider(logger) -> bool:
    """Check the local/remote HTTP PO-token provider before a download run."""
    ping_url = f"{POT_PROVIDER_URL.rstrip('/')}/ping"
    try:
        # Do not inherit an outbound proxy for a normally local provider.
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with opener.open(ping_url, timeout=3) as response:
            healthy = 200 <= response.status < 300
    except Exception as exc:
        logger.error("PO-token provider is unavailable at %s: %s", ping_url, exc)
        return False
    if healthy:
        logger.debug("PO-token provider is healthy at %s", ping_url)
    return healthy


def is_retryable_youtube_failure(error: DownloadCommandError) -> bool:
    """Return whether another cookie-free client/format may help."""
    message = error.stderr.lower()
    return any(
        marker in message
        for marker in (
            "http error 403",
            "requested format is not available",
            "no video formats found",
            "no formats found",
        )
    )


def is_members_only_error(error: object) -> bool:
    """Identify YouTube's explicit channel-members access restriction."""
    # DownloadCommandError deliberately has a concise __str__, while yt-dlp's
    # useful explanation is retained in stderr.
    message = " ".join(
        part
        for part in (str(error), getattr(error, "stderr", ""))
        if part
    ).lower()
    return (
        "available to this channel's members" in message
        or "members-only content" in message
    )


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
                        print(traceback.format_exc())
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
                        print(traceback.format_exc())
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
                        print(traceback.format_exc())

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
@click.option("--proxy", help="Override database proxies for this run")
@click.option("--random_sort", is_flag=True, help="Sort sources randomly")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.option(
    "--dry-run", is_flag=True, help="Show what would be downloaded without downloading"
)
def download_youtube(
    source_id: Optional[int],
    url: Optional[str],
    tg_channel: Optional[int],
    quality: str,
    proxy: Optional[str],
    random_sort: bool,
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
            if not dry_run and not check_pot_provider(logger):
                logger.warning(
                    "PO-token provider is not running; tv_simply and other "
                    "non-PO-token strategies can still be attempted. Start it "
                    "with scripts/start-pot-provider.sh to enable mweb fallback"
                )
            if proxy and not is_valid_proxy(proxy):
                raise click.UsageError(
                    "--proxy must be an HTTP URL such as http://user:pass@ip:port"
                )
            proxy_candidates = [proxy] if proxy else await ProxyService.get_urls_randomized()
            if not proxy_candidates:
                proxy_candidates = [None]
            selected_proxy = proxy_candidates[0]
            logger.info("Download network route: %s", redact_proxy(selected_proxy))
            if not selected_proxy:
                logger.warning("No proxy is configured; downloads will use a direct connection")
            tg_channel_obj = None
            # Handle single URL download
            if url:
                if dry_run:
                    click.echo(f"🔍 Would download from URL: {url}")
                    return

                # Ensure output directory exists
                os.makedirs(OUTPUT_DIR, exist_ok=True)

                downloaded = await download_single_url(
                    url,
                    tg_channel_obj,
                    quality,
                    verbose,
                    logger,
                    selected_proxy,
                    proxy_candidates,
                )
                if downloaded:
                    if downloaded.get("already_downloaded"):
                        click.echo(f"ℹ️ Already downloaded: {downloaded['title']}")
                    else:
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
            elif tg_channel:
                print(f"Processing only for tg channel: [{tg_channel}]")
                sources = await SourceService.get_by_channel_id(
                    tg_channel_id=tg_channel
                )
            else:
                if random_sort:
                    print("Sorting sources randomly")
                    sources = await SourceService.get_all_random()
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
                        source, source.max_videos_per_channel, quality, verbose, logger,
                        selected_proxy,
                        proxy_candidates,
                    )
                    total_downloaded += downloaded_count

                    if verbose:
                        click.echo(
                            f"✅ Downloaded {downloaded_count} from {source.name}"
                        )

                except Exception as e:
                    logger.error(f"Error processing source {source.name}: {e}")
                    click.echo(f"❌ Error processing {source.name}: {e}")
                    print(traceback.format_exc())

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
        print(traceback.format_exc())
        return

    try:
        audio.add_tags()
    except error:
        # print(traceback.format_exc())
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
        print(traceback.format_exc())

        logging.getLogger(__name__).warning(f"Error embedding metadata: {e}")
        return False


async def process_channel_download(
    source, max_videos: int, quality: str, verbose: bool, logger,
    proxy: Optional[str] = None,
    proxy_candidates: Optional[list[Optional[str]]] = None,
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
            # "--cookies-from-browser",
            # "chromium:Default",
            # "--cookies",
            # "/tmp/cookies.txt",
            # "--extractor-args",
            # "youtube:player-client=android_vr",
            "--dump-json",
            "--flat-playlist",
            "--playlist-end",
            str(max_videos),
            source.url,
        ]
        add_youtube_extractor_arguments(cmd, logger)
        add_proxy_argument(cmd, proxy)
        process = run_download_command(cmd, logger, "channel discovery", proxy)
        videos = [
            json.loads(line) for line in process.stdout.splitlines() if line.strip()
        ]

        total_videos = len(videos)
        downloaded_count = 0
        print(f"Processing {total_videos} videos...")
        for video in videos:
            # Check if already exists
            podcast = await Podcast.filter(yt_id=video["id"]).first()
            if podcast:
                if podcast.is_downloaded:
                    print(f"Podcast already downloaded: {podcast}, skipping")
                    continue
                elif not podcast.is_active:
                    logger.info("Podcast is inactive, skipping: %s", podcast.name)
                    continue
                else:
                    print(f"Downloading previously added podcast: {podcast}")
                    time.sleep(random.randint(1, 3))

            video_url = f"https://www.youtube.com/watch?v={video['id']}"
            print(f"Video url: {video_url}")

            # Get video info
            video_info = get_video_info(video_url, proxy, logger)
            if not video_info or "error" in video_info:
                error = video_info.get("error", "unknown error") if video_info else "unknown error"
                if is_members_only_error(error):
                    logger.info(
                        "Marking members-only video inactive: video_id=%s url=%s",
                        video["id"],
                        video_url,
                    )
                    if podcast:
                        podcast.is_active = False
                        await podcast.save()
                    else:
                        nd = await PodcastService.get_next_publication_date()
                        await PodcastService.create(
                            {
                                "name": video.get("title") or video["id"],
                                "description": video.get("description", ""),
                                "url": video_url,
                                "source_id": source.id,
                                "tg_channel_id": source.tg_channel_id,
                                "yt_id": video["id"],
                                "publication_date": nd,
                                "is_active": False,
                                "is_processed": False,
                                "file": None,
                                "duration": video.get("duration"),
                                "is_posted": False,
                                "is_downloaded": False,
                                "thumbnail_url": video.get("thumbnail", ""),
                            }
                        )
                print(f"Did not get video info {video_info}")
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
                podcast = await PodcastService.create(podcast_data)
                logger.info(f"New podcast: {podcast}")

            elif podcast.is_downloaded:
                print("Podcast already downloaded, skiping")
                continue

            duration = video_info.get("duration")
            if duration is None:
                logger.warning(
                    "Skipping video because yt-dlp returned no duration: "
                    "video_id=%s url=%s title=%r",
                    video_info.get("id"),
                    video_url,
                    video_info.get("title"),
                )
                continue

            try:
                duration = int(duration)
            except (TypeError, ValueError):
                logger.warning(
                    "Skipping video because yt-dlp returned an invalid duration: "
                    "video_id=%s duration=%r url=%s",
                    video_info.get("id"),
                    duration,
                    video_url,
                )
                continue

            if duration < source.min_duration or duration > source.max_duration:
                print(
                    f"Video is too small or too big: {duration // 60} min {duration % 60 } seconds"
                )
                podcast.is_active = False
                await podcast.save()
                continue

            # Check banned words
            title_lower = video_info["title"].lower()
            if any(bn.name.lower() in title_lower for bn in banned_words):
                print(f"Banned word found, skiping video")
                podcast.is_active = False
                await podcast.save()

                continue

            if not podcast.is_active:
                logger.info(f"Podcast is inactive, skipping download: {podcast.name}")
                continue

            # Check theme if needed
            if source.only_related:
                if not await PodcastService.check_theme(id=podcast.id):
                    print("Not relevant podcast: {podcast}, skipping")
                    continue

            if podcast.is_active:
                # Download
                logger.info(f"Downloading new audio: {video_url}: {podcast.name}")
                try:
                    downloaded = download_audio_with_retries(
                        video_url,
                        channel_dir,
                        quality,
                        proxy_candidates or [proxy],
                        logger,
                    )
                except MembersOnlyVideoError:
                    logger.info(
                        "Marking members-only video inactive: video_id=%s url=%s",
                        video["id"],
                        video_url,
                    )
                    podcast.is_active = False
                    await podcast.save()
                    continue
                time.sleep(10)
            else:
                downloaded = False
                logger.info(f"Not downloading - {podcast.name}")
            if downloaded:
                # Download thumbnail
                thumbnail_path = f"{downloaded.get('file_path')}-thumb.jpg"
                async with aiohttp.ClientSession() as session:
                    successful_proxy = downloaded.get("proxy")
                    logger.debug(
                        "Downloading thumbnail via %s",
                        redact_proxy(successful_proxy),
                    )
                    async with session.get(
                        podcast.thumbnail_url, proxy=successful_proxy
                    ) as response:
                        logger.debug("Thumbnail response status: %s", response.status)
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
        print(traceback.format_exc())
        return 0


def get_video_info(url, proxy: Optional[str] = None, logger=None):
    """Get video information using yt-dlp."""
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        # Metadata extraction must not depend on yt-dlp finding a format that
        # matches its default download selector. The actual audio download
        # below has its own client/format fallback strategies.
        "ignore_no_formats_error": True,
        "remote_components": ["ejs:github"],
        "extractor_args": {
            "youtube": {
                "player_client": [YOUTUBE_PLAYER_CLIENT],
                "pot_trace": ["true"],
            },
            "youtubepot-bgutilhttp": {"base_url": [POT_PROVIDER_URL]},
        },
        # "extractor-args": "youtube:player-client=android_vr",
        # "cookiesfrombrowser": (
        #    "chromium",
        #    "Default",
        # ),
        # "cookies_from_browser": "chromium" "Default",
        # "cookies": "/tmp/cookies.txt",
        # "--extractor-args",
        # "youtube:player-client=default,tv"
    }
    if proxy:
        ydl_opts["proxy"] = proxy
    if logger:
        ydl_opts["verbose"] = logger.isEnabledFor(logging.DEBUG)
        logger.debug("Extracting video metadata for %s via %s", url, redact_proxy(proxy))
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
        print(traceback.format_exc())

        return {"error": str(e)}


def download_audio(video_url, output_path, quality="64", proxy=None, logger=None):
    """Download YouTube video as MP3."""
    try:
        logger = logger or logging.getLogger(__name__)
        os.makedirs(output_path, exist_ok=True)
        logger.debug("Download output directory: %s", os.path.abspath(output_path))

        # Get video info first
        info_cmd = [
            "yt-dlp",
            "--dump-json",
            "--ignore-no-formats-error",
            # "--cookies-from-browser",
            # "firefox",
            # "--cookies-from-browser",
            # "chromium:Default",
            # "--cookies",
            # "/tmp/cookies.txt",
            # "--extractor-args",
            # "youtube:player-client=android_vr",
            "--no-playlist",
            video_url,
        ]
        add_youtube_extractor_arguments(info_cmd, logger)
        add_proxy_argument(info_cmd, proxy)
        info_process = run_download_command(info_cmd, logger, "video metadata", proxy)
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

        # Download command. A valid PO token can still be rejected for one
        # client/format/CDN combination, so retry cookie-free alternatives
        # before giving up on the current network route.
        output_template = os.path.join(output_path, "%(id)s.%(ext)s")
        strategies = [
            (YOUTUBE_PLAYER_CLIENT, "bestaudio"),
            *((client, "bestaudio/best") for client in YOUTUBE_FALLBACK_CLIENTS),
        ]
        last_error = None
        print("Downloading...")
        print("=" * 20)
        for strategy_number, (player_client, format_selector) in enumerate(
            strategies, start=1
        ):
            cmd = [
                "yt-dlp",
                "-f",
                format_selector,
                "--extract-audio",
                "--audio-format",
                "mp3",
                "--audio-quality",
                quality,
                "--embed-thumbnail",
                "--add-metadata",
                "--no-playlist",
                "-o",
                output_template,
                video_url,
            ]
            add_youtube_extractor_arguments(cmd, logger, player_client)
            add_proxy_argument(cmd, proxy)
            logger.info(
                "YouTube strategy %s/%s: client=%s format=%s",
                strategy_number,
                len(strategies),
                player_client,
                format_selector,
            )
            try:
                run_download_command(
                    cmd,
                    logger,
                    f"audio download ({player_client}, {format_selector})",
                    proxy,
                )
                last_error = None
                break
            except DownloadCommandError as exc:
                last_error = exc
                if not is_retryable_youtube_failure(exc):
                    raise
                logger.warning(
                    "YouTube strategy failed: client=%s format=%s",
                    player_client,
                    format_selector,
                )
        if last_error:
            raise last_error
        print("Done")
        print("=" * 20)
        # Check for output file
        expected_filename = f"{video_info.get('id')}.mp3"
        expected_path = os.path.join(output_path, expected_filename)
        logger.debug("Expected downloaded file: %s", os.path.abspath(expected_path))
        time.sleep(4)
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
            print(f"File not found: {expected_path}")

        return None
    except Exception as exc:
        if is_members_only_error(exc):
            raise MembersOnlyVideoError(
                f"Channel membership is required for {video_url}"
            ) from exc
        print(traceback.format_exc())
        return None


def download_audio_with_retries(
    video_url: str,
    output_path: str,
    quality: str,
    proxies: list[Optional[str]],
    logger,
):
    """Try an audio download through each configured proxy in order."""
    attempts = proxies or [None]
    for attempt, candidate in enumerate(attempts, start=1):
        logger.info(
            "Audio download attempt %s/%s via %s",
            attempt,
            len(attempts),
            redact_proxy(candidate),
        )
        downloaded = download_audio(
            video_url, output_path, quality, candidate, logger
        )
        if downloaded:
            downloaded["proxy"] = candidate
            if attempt > 1:
                logger.info(
                    "Audio download succeeded after proxy rotation via %s",
                    redact_proxy(candidate),
                )
            return downloaded
        logger.warning(
            "Audio download attempt failed via %s",
            redact_proxy(candidate),
        )

    logger.error(
        "Audio download failed through all %s configured network routes: %s",
        len(attempts),
        video_url,
    )
    return None


async def download_single_url(
    url: str, tg_channel_obj, quality: str, verbose: bool, logger,
    proxy: Optional[str] = None,
    proxy_candidates: Optional[list[Optional[str]]] = None,
) -> dict:
    """Download a single URL and create podcast entry."""
    try:
        # Get video info
        video_info = get_video_info(url, proxy, logger)
        if not video_info or "error" in video_info:
            logger.error(f"Failed to get video info for {url}")
            return None

        # Check if podcast already exists
        existing_podcast = await Podcast.filter(url=url).first()
        if existing_podcast:
            logger.info(f"Podcast already exists: {existing_podcast.name}")
            existing_file = existing_podcast.file
            if (
                existing_podcast.is_downloaded
                and existing_file
                and os.path.isfile(existing_file)
            ):
                return {
                    "title": existing_podcast.name,
                    "id": existing_podcast.id,
                    "already_downloaded": True,
                }
            logger.warning(
                "Existing podcast has no downloaded file; retrying download: id=%s file=%r",
                existing_podcast.id,
                existing_file,
            )

        # Create directory for download
        download_dir = os.path.join(OUTPUT_DIR, "single_downloads")

        # Download the audio
        logger.info(f"Downloading: {video_info.get('title')}")
        downloaded = download_audio_with_retries(
            url, download_dir, quality, proxy_candidates or [proxy], logger
        )

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

        if existing_podcast:
            for field, value in podcast_data.items():
                if field not in {"source_id", "tg_channel_id"}:
                    setattr(existing_podcast, field, value)
            if tg_channel_obj:
                existing_podcast.tg_channel_id = tg_channel_obj.id
            await existing_podcast.save()
            podcast = existing_podcast
            logger.info("Updated existing podcast after download: %s", podcast.name)
        else:
            podcast = await PodcastService.create(podcast_data)

        # Download thumbnail
        if video_info.get("thumbnail"):
            thumbnail_path = f"{downloaded.get('file_path')}-thumb.jpg"
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    video_info.get("thumbnail"), proxy=downloaded.get("proxy")
                ) as response:
                    logger.debug("Thumbnail response status: %s", response.status)
                    if response.status == 200:
                        with open(thumbnail_path, "wb") as f:
                            f.write(await response.read())

                        # Update podcast with thumbnail path
                        podcast.thumbnail = thumbnail_path
                        await podcast.save()

        logger.info(f"Saved downloaded podcast: {podcast.name}")

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
# 9m yGg)_r~/hDU9m)4j
