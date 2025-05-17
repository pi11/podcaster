# run.py
import argparse
import asyncio
import os
import sys

from sanic import Sanic
from app.main import app


def parse_args():
    parser = argparse.ArgumentParser(description="Run the Sanic Tortoise application")
    parser.add_argument(
        "--host",
        default=os.getenv("HOST", "0.0.0.0"),
        help="Host to bind the server to",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("PORT", 8000)),
        help="Port to bind the server to",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=int(os.getenv("WORKERS", 1)),
        help="Number of worker processes",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=os.getenv("DEBUG", "False").lower() == "true",
        help="Enable debug mode",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Configure Sanic
    app.config.update(
        {
            "HOST": args.host,
            "PORT": args.port,
            "WORKERS": args.workers,
            "DEBUG": args.debug,
        }
    )

    print(
        f"Starting Sanic application on {args.host}:{args.port} with {args.workers} workers (Debug: {args.debug})"
    )

    # Run the application
    app.run(
        host=args.host,
        port=args.port,
        workers=args.workers,
        debug=args.debug,
        access_log=args.debug,
        auto_reload=args.debug,
    )


if __name__ == "__main__":
    main()
