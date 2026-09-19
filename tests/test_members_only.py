import logging

import pytest

from app import cli


MEMBERS_ONLY_MESSAGE = (
    "ERROR: [youtube] UMtvvBiqw3c: This video is available to this channel's "
    "members on level: Tomato (or any higher level). Join this channel to get "
    "access to members-only content and other exclusive perks."
)


def test_members_only_error_reads_download_command_stderr():
    error = cli.DownloadCommandError("video metadata", 1, MEMBERS_ONLY_MESSAGE)

    assert cli.is_members_only_error(error)


def test_download_audio_propagates_members_only_error(monkeypatch, tmp_path):
    def fail_command(*args, **kwargs):
        raise cli.DownloadCommandError("video metadata", 1, MEMBERS_ONLY_MESSAGE)

    monkeypatch.setattr(cli, "run_download_command", fail_command)

    with pytest.raises(cli.MembersOnlyVideoError):
        cli.download_audio(
            "https://www.youtube.com/watch?v=UMtvvBiqw3c",
            str(tmp_path),
            logger=logging.getLogger("test"),
        )


def test_unrelated_download_error_is_not_members_only():
    error = cli.DownloadCommandError("audio download", 1, "HTTP Error 403")

    assert not cli.is_members_only_error(error)
