import logging
from types import SimpleNamespace

import pytest
from sanic import response
from tortoise import Tortoise

from app import cli
from app.models import Source, TgChannel
from app.routes import main
from app.services import SourceService


CHANNEL_404 = (
    "WARNING: [youtube:tab] HTTP Error 404: Not Found. Retrying (1/3)...\n"
    "ERROR: [youtube:tab] @missing: Unable to download webpage: "
    "HTTP Error 404: Not Found"
)
CHANNEL_404_AFTER_RETRIES = (
    "WARNING: [youtube:tab] HTTP Error 404: Not Found. Retrying (1/3)...\n"
    "WARNING: [youtube:tab] Unable to download webpage: HTTP Error 404: "
    "Not Found. Giving up after 3 retries\n"
    "ERROR: [youtube:tab] @missing: Failed to resolve url "
    "(does the playlist exist?)"
)


def test_only_terminal_channel_404_disables_source():
    assert cli.is_missing_youtube_channel(
        cli.DownloadCommandError("channel discovery", 1, CHANNEL_404)
    )
    assert cli.is_missing_youtube_channel(
        cli.DownloadCommandError("channel discovery", 1, CHANNEL_404_AFTER_RETRIES)
    )
    assert not cli.is_missing_youtube_channel(
        cli.DownloadCommandError(
            "channel discovery", 1, CHANNEL_404.splitlines()[0]
        )
    )
    assert not cli.is_missing_youtube_channel(
        cli.DownloadCommandError("video metadata", 1, CHANNEL_404)
    )


@pytest.mark.asyncio
async def test_terminal_channel_404_disables_source_until_reenabled(monkeypatch):
    await Tortoise.init(db_url="sqlite://:memory:", modules={"models": ["app.models"]})
    await Tortoise.generate_schemas()
    try:
        channel = await TgChannel.create(name="Target", tg_id="-1001")
        source = await Source.create(
            name="Missing", url="https://www.youtube.com/@missing/videos",
            tg_channel_id=channel.id,
        )
        other = await Source.create(
            name="Working", url="https://www.youtube.com/@working/videos",
            tg_channel_id=channel.id,
        )

        async def no_banned_words():
            return []

        def missing_channel(*args, **kwargs):
            raise cli.DownloadCommandError(
                "channel discovery", 1, CHANNEL_404_AFTER_RETRIES
            )

        monkeypatch.setattr(cli.BannedWordsService, "get_all", no_banned_words)
        monkeypatch.setattr(cli, "run_download_command", missing_channel)
        count = await cli.process_channel_download(
            source, 1, "64", False, logging.getLogger("test")
        )
        assert count == 0
        await source.refresh_from_db()
        assert source.is_active is False
        assert [s.id for s in await SourceService.get_all(active_only=True)] == [other.id]
        assert [s.id for s in await SourceService.get_by_channel_id(
            channel.id, active_only=True
        )] == [other.id]

        async def fake_render(template, context):
            assert template == "sources/row.html"
            assert context["source"].is_active is True
            return response.text("enabled row")

        monkeypatch.setattr(main, "render", fake_render)
        result = await main.sources_toggle(
            SimpleNamespace(headers={"HX-Request": "true"}), source.id
        )
        assert result.status == 200
        await source.refresh_from_db()
        assert source.is_active is True
    finally:
        await Tortoise.close_connections()


@pytest.mark.asyncio
async def test_retry_warning_without_terminal_404_keeps_source_active(monkeypatch):
    await Tortoise.init(db_url="sqlite://:memory:", modules={"models": ["app.models"]})
    await Tortoise.generate_schemas()
    try:
        source = await Source.create(
            name="Retried", url="https://www.youtube.com/@retried/videos"
        )

        async def no_banned_words():
            return []

        def successful_retry(*args, **kwargs):
            return SimpleNamespace(stdout="", stderr=CHANNEL_404.splitlines()[0])

        monkeypatch.setattr(cli.BannedWordsService, "get_all", no_banned_words)
        monkeypatch.setattr(cli, "run_download_command", successful_retry)
        assert await cli.process_channel_download(
            source, 1, "64", False, logging.getLogger("test")
        ) == 0
        await source.refresh_from_db()
        assert source.is_active is True
    finally:
        await Tortoise.close_connections()
