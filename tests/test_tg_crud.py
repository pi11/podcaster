from types import SimpleNamespace

import pytest
from sanic import response
from tortoise import Tortoise

from app.models import TgChannel
from app.routes import main


def request(form, *, htmx=False):
    return SimpleNamespace(
        form=form,
        headers={"HX-Request": "true"} if htmx else {},
    )


@pytest.mark.asyncio
async def test_tg_channels_can_be_created_edited_and_deleted(monkeypatch):
    await Tortoise.init(db_url="sqlite://:memory:", modules={"models": ["app.models"]})
    await Tortoise.generate_schemas()
    try:
        created = await main.tg_create(request({"id": " -1001 ", "name": " Old "}))
        assert created.status == 302
        channel = await TgChannel.get(tg_id="-1001")
        assert channel.name == "Old"
        assert channel.auto_post is False

        async def fake_render(template, context):
            assert template == "tg/row.html"
            assert context["tg"].id == channel.id
            return response.text("updated row")

        monkeypatch.setattr(main, "render", fake_render)
        updated = await main.tg_update(
            request({"id": "-1002", "name": "New", "auto_post": "check"}, htmx=True),
            channel.id,
        )
        assert updated.status == 200
        await channel.refresh_from_db()
        assert (channel.tg_id, channel.name, channel.auto_post) == ("-1002", "New", True)

        updated = await main.tg_update(
            request({"id": "-1002", "name": "Renamed"}), channel.id
        )
        assert updated.status == 302
        await channel.refresh_from_db()
        assert (channel.name, channel.auto_post) == ("Renamed", False)

        deleted = await main.tg_delete(request({}, htmx=True), channel.id)
        assert deleted.status == 200
        assert not await TgChannel.filter(id=channel.id).exists()
    finally:
        await Tortoise.close_connections()


@pytest.mark.asyncio
async def test_tg_edit_rejects_duplicate_or_missing_values():
    await Tortoise.init(db_url="sqlite://:memory:", modules={"models": ["app.models"]})
    await Tortoise.generate_schemas()
    try:
        first = await TgChannel.create(name="First", tg_id="-1001")
        second = await TgChannel.create(name="Second", tg_id="-1002")

        duplicate = await main.tg_update(
            request({"id": first.tg_id, "name": "Changed"}), second.id
        )
        assert duplicate.status == 400
        await second.refresh_from_db()
        assert (second.tg_id, second.name) == ("-1002", "Second")

        invalid = await main.tg_update(
            request({"id": " ", "name": "Changed"}), second.id
        )
        assert invalid.status == 400
        missing = await main.tg_update(
            request({"id": "-1003", "name": "New"}), 9999
        )
        assert missing.status == 404
        invalid_create = await main.tg_create(request({"id": "", "name": "New"}))
        assert invalid_create.status == 400
    finally:
        await Tortoise.close_connections()
