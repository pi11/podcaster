"""
Run the GMP Sanic application.
"""

from app.config.settings import settings
from app import create_app

app = create_app(settings)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=settings.DEBUG)
