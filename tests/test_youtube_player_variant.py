import logging

from app import cli


def test_download_paths_use_tv_player_variant(monkeypatch):
    command = ["yt-dlp"]
    cli.add_youtube_extractor_arguments(command, logging.getLogger("test"))
    extractor_args = command[command.index("--extractor-args") + 1]
    assert "player_js_variant=tv" in extractor_args

    options = {}

    class FakeYoutubeDL:
        def __init__(self, ydl_opts):
            options.update(ydl_opts)

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def extract_info(self, url, download):
            return {"id": "example"}

    monkeypatch.setattr(cli.yt_dlp, "YoutubeDL", FakeYoutubeDL)
    assert cli.get_video_info("https://www.youtube.com/watch?v=example")["id"] == "example"
    assert options["extractor_args"]["youtube"]["player_js_variant"] == ["tv"]
