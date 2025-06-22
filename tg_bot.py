"""
Telegram Bot for Podcast Manager
This script runs a Telegram bot that can post podcasts to a Telegram channel.
"""

import os
import logging
import traceback
import asyncio
from datetime import datetime
import json
from tortoise import Tortoise
import telegram
from telegram.ext import Application, CommandHandler, CallbackContext
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

from telegram import Update

# App specific imports
from app.models import Podcast, Category, CategoryIdentification
from app.services import PodcastService, CategoryService, CategoryIdentificationService
from app.config import TG_TOKEN, TG_CHANNEL
from app.utils.helpers import close_db, init_db, extract_hashtags

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("telegram_bot.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        "Hi! I am the Podcast Manager bot. \nUse /help to see available commands."
    )


async def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    help_text = (
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/post Post next podcast to the channel\n"
        "/status - Show bot status and configuration"
    )
    await update.message.reply_text(help_text)


async def status_command(update: Update, context: CallbackContext) -> None:
    """Show bot status and configuration."""

    channel_id = TG_CHANNEL

    # Count total and pending podcasts
    try:
        await init_db()
        total_count = await PodcastService.count()
        pending_count = await PodcastService.count(is_posted=False)

        status_text = (
            f"🤖 Bot Status:\n\n"
            f"Telegram Channel: {channel_id}\n"
            f"Total Podcasts: {total_count}\n"
            f"Pending Podcasts: {pending_count}\n"
        )

        await update.message.reply_text(status_text)
    except Exception as e:
        logger.error(f"Error in status command: {e}")
        await update.message.reply_text(f"Error getting status: {str(e)}")
    finally:
        await close_db()


async def post_telegram(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Post a specific podcast to the channel."""
    # Check if podcast_id is provided

    try:
        await init_db()

        # Get the podcast
        podcast = await PodcastService.get_post()  # ready for posting podcasts
        if not podcast:
            print("No podcasts for posting, skip for now")
            return
        # Post to channel
        source = await podcast.source
        channel = await podcast.tg_channel
        success = await post_podcast_to_telegram(podcast, context.bot, channel.tg_id)

        if success:
            # Update podcast status if it was successfully posted
            if not podcast.is_posted:
                podcast.is_posted = True
                await podcast.save()

                print(f"Podcast '{podcast.name}' posted to channel successfully.")

        else:
            print(f"Failed to post podcast '{podcast.name}' to channel.")
            if podcast.failed_times > 3:
                print("Failed 4 times, mark podcast as inactive")
                podcast.is_active = False
                await podcast.save()
            else:
                podcast.failed_times += 1
                await podcast.save()

    except Exception as e:
        logger.error(f"Error in post command: {e}")
        print(traceback.format_exc())
        print(f"Error posting podcast: {str(e)}")
    finally:
        await close_db()


async def post_podcast_to_telegram(podcast, bot, channel_id):
    """
    Post a podcast to the Telegram channel

    Args:
        podcast: Podcast object
        bot: Telegram bot instance
        channel_id: Channel ID to post to

    Returns:
        bool: True if successful, False otherwise
    """
    if not podcast:
        print("No podcast")
    else:
        print(f"Podcast: {podcast}")
    try:
        # Format the message according to requirements
        message = f"{podcast.name}\n{podcast.url}\n"
        cats = await podcast.categories
        source = await podcast.source
        if source:
            message += "\n"
            hashtag = "#" + source.name.replace(" ", "").replace("'", "").lower()
            message += f"{hashtag} "

        hashtags = [c.name.replace(" ", "").lower().strip() for c in cats]
        if source:
            if source.extract_tags:
                # also extract tags from description
                hashtags += extract_hashtags(podcast.description)
        else:  # by default extraxt tags anyway
            hashtags += extract_hashtags(podcast.description)

        proc_hashtags = [h.lower().strip() for h in hashtags]
        hashtags = list(set(proc_hashtags))

        for hashtag in hashtags[:8]:  # max 8 hash tags
            message += f"#{hashtag.lower()} "

        with open(podcast.file, "rb") as audio:
            if os.path.exists(podcast.thumbnail):
                thumbnail = open(podcast.thumbnail, "rb")
                print("Posting with thumbnail!")
            else:
                print("Posting without thumb")
                thumbnail = None

            await bot.send_audio(
                chat_id=channel_id,
                audio=audio,
                caption=message,
                title=podcast.name,
                thumbnail=thumbnail,
                read_timeout=30,  # Read timeout in seconds
                write_timeout=50,  # Write timeout in seconds
                connect_timeout=10,
            )
        logger.info(f"Posted podcast '{podcast.name}' to Telegram channel")
        podcast.is_posted = True
        podcast.publication_date = datetime.now()
        await podcast.save()
        return True

    except Exception as e:
        logger.error(f"Failed to post podcast to Telegram: {e}")
        print(traceback.format_exc())
        return False


async def error_handler(update: Update, context: CallbackContext) -> None:
    """Log the error and send a message to the user."""
    logger.error(f"Exception while handling an update: {context.error}")

    if update and update.effective_message:
        await update.effective_message.reply_text(
            "An error occurred while processing your request. Please try again later."
        )


async def post_job(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Job to post awaited"""
    print("hello")
    logger.info("Scheduled job: hello")


def main():
    """Start the bot."""
    # Load configuration

    token = TG_TOKEN
    if not token:
        logger.error("Bot token not found in configuration. Exiting.")
        return

    # Create the Application
    application = Application.builder().token(token).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    # application.add_handler(CommandHandler("status", status_command))
    # application.add_handler(CommandHandler("post", post_command))

    # Add error handler
    application.add_error_handler(error_handler)

    job_queue = application.job_queue
    job_minute = job_queue.run_repeating(post_telegram, interval=30, first=10)

    # Start the Bot
    logger.info("Starting Telegram Bot")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
