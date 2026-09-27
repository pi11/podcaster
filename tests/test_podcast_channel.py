from datetime import datetime
from types import SimpleNamespace

import pytest
from tortoise import Tortoise

from app.models import Podcast, TgChannel
from app.routes.main import podcasts_update_channel
from app.services import PodcastService


@pytest.mark.asyncio
async def test_podcast_channel_can_be_changed_and_cleared():
    await Tortoise.init(db_url="sqlite://:memory:", modules={"models": ["app.models"]})
    await Tortoise.generate_schemas()
    try:
        old_channel = await TgChannel.create(name="Old", tg_id="-1001")
        new_channel = await TgChannel.create(name="New", tg_id="-1002")
        podcast = await Podcast.create(
            name="Episode",
            url="https://example.com/episode",
            yt_id="episode",
            publication_date=datetime(2026, 1, 1),
            tg_channel_id=old_channel.id,
            is_processed=True,
        )
        assert [p.id for p in await PodcastService.get_relevant(old_channel.id)] == [
            podcast.id
        ]

        request = SimpleNamespace(
            form={"tg_channel_id": str(new_channel.id)},
            args={"tg_id": str(old_channel.id)},
        )
        result = await podcasts_update_channel(request, podcast.id)
        await podcast.refresh_from_db()
        assert result.status == 302
        assert result.headers["Location"] == f"/podcasts?tg_id={old_channel.id}"
        assert podcast.tg_channel_id == new_channel.id
        assert await old_channel.count() == 0
        assert await new_channel.count() == 1
        assert await PodcastService.get_relevant(old_channel.id) == []
        assert [p.id for p in await PodcastService.get_relevant(new_channel.id)] == [
            podcast.id
        ]

        request.form["tg_channel_id"] = "9999"
        result = await podcasts_update_channel(request, podcast.id)
        await podcast.refresh_from_db()
        assert result.status == 400
        assert podcast.tg_channel_id == new_channel.id

        request.args = {
            "tg_id": str(old_channel.id),
            "under_50mb": "1",
            "page": "2",
        }
        request.form["tg_channel_id"] = ""
        result = await podcasts_update_channel(request, podcast.id)
        await podcast.refresh_from_db()
        assert result.status == 302
        assert result.headers["Location"] == (
            f"/podcasts?tg_id={old_channel.id}&under_50mb=1&page=2"
        )
        assert podcast.tg_channel_id is None
    finally:
        await Tortoise.close_connections()
