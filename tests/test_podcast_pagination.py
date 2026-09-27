from datetime import datetime, timedelta
from types import SimpleNamespace

import pytest
from tortoise import Tortoise

from app.models import Podcast, Source, TgChannel
from app.routes import main
from app.services import PodcastService


@pytest.mark.asyncio
async def test_podcast_pagination_and_size_filter(monkeypatch):
    await Tortoise.init(db_url="sqlite://:memory:", modules={"models": ["app.models"]})
    await Tortoise.generate_schemas()
    try:
        channel = await TgChannel.create(name="Channel", tg_id="-1003")
        source = await Source.create(
            name="Source", url="https://example.com/source", tg_channel_id=channel.id
        )
        for index in range(26):
            await Podcast.create(
                name=f"Episode {index}",
                url=f"https://example.com/episode/{index}",
                yt_id=f"episode-{index}",
                publication_date=datetime(2026, 1, 1) + timedelta(minutes=index),
                tg_channel_id=channel.id,
                source_id=source.id,
                filesize=49_999_999 if index < 23 else 50_000_000,
                is_processed=True,
                is_posted=index == 25,
            )

        first, total, page, total_pages = await PodcastService.get_page(
            page=1, tg_id=channel.id
        )
        assert (total, page, total_pages, len(first)) == (25, 1, 2, 20)
        assert first[0].name == "Episode 0"

        second, total, page, total_pages = await PodcastService.get_page(
            page=99, tg_id=channel.id, under_50mb=True
        )
        assert (total, page, total_pages) == (23, 2, 2)
        assert [podcast.name for podcast in second] == [
            "Episode 20",
            "Episode 21",
            "Episode 22",
        ]

        source_page, source_total, _, _ = await PodcastService.get_page(
            page=1, source_id=source.id, under_50mb=True
        )
        assert source_total == 23
        assert len(source_page) == 20

        async def capture_render(template, context):
            assert template == "podcasts/list.html"
            return context

        monkeypatch.setattr(main, "render", capture_render)
        context = await main.podcasts_list(
            SimpleNamespace(
                args={
                    "tg_id": str(channel.id),
                    "under_50mb": "1",
                    "page": "2",
                }
            )
        )
        assert context["page"] == 2
        assert context["total"] == 23
        assert context["under_50mb"] is True
        assert context["return_query"] == (
            f"tg_id={channel.id}&under_50mb=1&page=2"
        )
        assert context["prev_url"] == (
            f"/podcasts?tg_id={channel.id}&under_50mb=1"
        )
    finally:
        await Tortoise.close_connections()
