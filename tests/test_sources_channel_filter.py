from types import SimpleNamespace

import pytest
from tortoise import Tortoise

from app.models import Source, TgChannel
from app.routes import main


@pytest.mark.asyncio
async def test_sources_page_filters_by_telegram_channel(monkeypatch):
    await Tortoise.init(db_url="sqlite://:memory:", modules={"models": ["app.models"]})
    await Tortoise.generate_schemas()
    try:
        first = await TgChannel.create(name="First", tg_id="-1001")
        second = await TgChannel.create(name="Second", tg_id="-1002")
        first_source = await Source.create(
            name="First source", url="https://example.com/first", tg_channel_id=first.id
        )
        second_source = await Source.create(
            name="Second source", url="https://example.com/second", tg_channel_id=second.id
        )

        async def capture_render(template, context):
            assert template == "sources/list.html"
            return context

        monkeypatch.setattr(main, "render", capture_render)

        filtered = await main.sources_list(
            SimpleNamespace(args={"channel_id": str(first.id)})
        )
        assert filtered["channel_id"] == first.id
        assert [item["source"].id for item in filtered["sources"]] == [
            first_source.id
        ]
        assert {tg.id for tg in filtered["tgs"]} == {first.id, second.id}

        unfiltered = await main.sources_list(SimpleNamespace(args={}))
        assert {item["source"].id for item in unfiltered["sources"]} == {
            first_source.id,
            second_source.id,
        }
        empty = await main.sources_list(SimpleNamespace(args={"channel_id": "9999"}))
        assert empty["sources"] == []
    finally:
        await Tortoise.close_connections()
