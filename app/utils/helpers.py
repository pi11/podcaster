"""Misc helpers"""

from app.config import STATIC_URL


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
