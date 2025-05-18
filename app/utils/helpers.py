"""Misc helpers"""

import logging
from tortoise import Tortoise

from app.config import STATIC_URL, TORTOISE_ORM

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("youtube_downloader.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


# Basic and random helper functions


def to_int(value):
    """Convert a value to integer or return None if conversion fails."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def inject_template_context(context):
    """Inject common settings into template context."""
    context["STATIC_URL"] = STATIC_URL
    return context


async def init_db():
    """Initialize database connection"""
    logger.info("Initializing database connection")

    await Tortoise.init(config=TORTOISE_ORM)
    logger.info("Database connection established")


async def close_db():
    """Close database connection"""
    logger.info("Closing database connection")
    await Tortoise.close_connections()


def humanizeTimeDiff(timestamp=None):
    """
    Возвращает человекопонятную строку разницы во времени между сейчас и timestamp.
    Поддерживает даты с таймзоной и будущие даты.
    """
    import datetime

    if timestamp is None:
        return "Неизвестно"

    now = (
        datetime.datetime.now(tz=timestamp.tzinfo)
        if timestamp.tzinfo
        else datetime.datetime.now()
    )
    is_future = timestamp > now
    time_diff = abs(now - timestamp)

    days = time_diff.days
    seconds = time_diff.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    months = days // 30
    years = days // 365

    def format_phrase(value, forms):
        """
        Возвращает правильное склонение в зависимости от числа
        forms = ('секунда', 'секунды', 'секунд')
        """
        if 11 <= value % 100 <= 14:
            form = forms[2]
        elif value % 10 == 1:
            form = forms[0]
        elif value % 10 in [2, 3, 4]:
            form = forms[1]
        else:
            form = forms[2]
        return f"через {value} {form}" if is_future else f"{value} {form} назад"

    if years > 0:
        return format_phrase(years, ("год", "года", "лет"))
    elif months > 0:
        return format_phrase(months, ("месяц", "месяца", "месяцев"))
    elif days > 0:
        return format_phrase(days, ("день", "дня", "дней"))
    elif hours > 0:
        return format_phrase(hours, ("час", "часа", "часов"))
    elif minutes > 0:
        return format_phrase(minutes, ("минута", "минуты", "минут"))
    elif seconds > 0:
        return format_phrase(seconds, ("секунда", "секунды", "секунд"))
    else:
        return "Только что"
