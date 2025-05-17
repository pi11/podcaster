"""Misc helpers"""

import random
from datetime import datetime

from tortoise import Tortoise

from app.config.settings import settings
from app.db.models import Video


# Basic and random helper functions


def to_int(value):
    """Convert a value to integer or return None if conversion fails."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return None
