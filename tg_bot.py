"""
Telegram Bot for Podcast Manager
This script runs a Telegram bot that can post podcasts to a Telegram channel.
"""

import os
import logging
import traceback
import asyncio
import datetime
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
from app.helpers.utils import close_db, init_db

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


async def post_command(update: Update, context: CallbackContext) -> None:
    """Post a specific podcast to the channel."""
    # Check if podcast_id is provided

    channel_id = TG_CHANNEL
    if not channel_id:
        await update.message.reply_text("Error: Channel ID not configured.")
        return

    try:
        await init_db()

        # Get the podcast
        podcast = await PodcastService.get_good()  # ready for posting podcasts
        if not podcast:
            await update.message.reply_text(f"No more podcast")
            return
        # Post to channel
        success = await post_podcast_to_telegram(podcast, context.bot, channel_id)

        if success:
            # Update podcast status if it was successfully posted
            if not podcast.is_posted:
                podcast.is_posted = True
                await podcast.save()

            await update.message.reply_text(
                f"Podcast '{podcast.name}' posted to channel successfully."
            )
        else:
            await update.message.reply_text(
                f"Failed to post podcast '{podcast.name}' to channel."
            )

    except Exception as e:
        logger.error(f"Error in post command: {e}")
        print(traceback.format_exc())
        await update.message.reply_text(f"Error posting podcast: {str(e)}")
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
        # Get category name if available
        category_name = None
        if hasattr(podcast, "source") and hasattr(podcast.source, "category"):
            category = await podcast.source.category
            if category:
                category_name = category.name

        # Format the message according to requirements
        message = f"{podcast.name}\nИсточник: {podcast.url}\n"

        # Add category hashtag if available
        if category_name:
            # Remove spaces and convert to lowercase for hashtag
            hashtag = "#" + category_name.replace(" ", "").lower()
            message += f"\n{hashtag}"

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
            )
        logger.info(f"Posted podcast '{podcast.name}' to Telegram channel")
        podcast.is_posted = True
        await podcast.save()
        return True

    except Exception as e:
        logger.error(f"Failed to post podcast to Telegram: {e}")
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
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("post", post_command))

    # Add error handler
    application.add_error_handler(error_handler)

    # Start the Bot
    logger.info("Starting Telegram Bot")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
