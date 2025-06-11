"""Models for gmp project"""

import os
import random
from datetime import datetime, timedelta
from enum import IntEnum
from typing import List
from slugify import slugify
from tortoise import fields, models
from app.utils.helpers import humanizeTimeDiff

# from tortoise.contrib.pydantic import pydantic_model_creator
# import pydantic

# from app.config import *


class Category(models.Model):
    """Video category"""

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        table = "category"


class CategoryIdentification(models.Model):
    """Category identification words"""

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    category = fields.ForeignKeyField("models.Category", related_name="identifications")

    def __str__(self):
        return self.name

    class Meta:
        table = "category_identification"


class BannedWords(models.Model):
    """Banned words"""

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        table = "banned_words"


class TgChannel(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    tg_id = fields.CharField(max_length=30, unique=True)
    auto_post = fields.BooleanField(default=False)

    # message_template = fields.CharField(max_length=250, default="{{ title }}\nИсточник: {{ url }}\n")
    def __str__(self):
        return self.name

    async def count(self):
        count = 0
        sources = await Source.filter(tg_channel=self.id)
        for source in sources:
            count += await Podcast.filter(
                source=source, is_active=True
            ).count()  # await source.count()
        return count

    class Meta:
        table = "tgchannel"


class Source(models.Model):
    """Sources (youtube channels)"""

    id = fields.IntField(pk=True)
    url = fields.CharField(max_length=500, unique=True)
    name = fields.CharField(max_length=200)
    min_duration = fields.IntField(default=0)
    max_duration = fields.IntField(default=10800)

    only_related = fields.BooleanField(
        default=False
    )  # if set, load only videos with related categories found
    tg_channel = fields.ForeignKeyField(
        "models.TgChannel", related_name="tg_channel", null=True
    )
    max_videos_per_channel = fields.IntField(default=15)

    extract_tags = fields.BooleanField(default=False)

    def __str__(self):
        return self.url

    class Meta:
        table = "source"


class Podcast(models.Model):
    id = fields.IntField(pk=True)
    url = fields.CharField(max_length=500, unique=True)
    yt_id = fields.CharField(max_length=25, unique=True)
    name = fields.CharField(max_length=500)
    description = fields.TextField(null=True)

    source = fields.ForeignKeyField("models.Source", related_name="source", null=True)
    tg_channel = fields.ForeignKeyField(
        "models.TgChannel", related_name="tgchannel", null=True
    )
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    publication_date = fields.DatetimeField()
    is_active = fields.BooleanField(default=True)
    is_posted = fields.BooleanField(default=False)
    is_awaiting_post = fields.BooleanField(default=False)
    is_processed = fields.BooleanField(default=False)
    is_downloaded = fields.BooleanField(default=False)

    file = fields.CharField(max_length=250, null=True)
    filesize = fields.IntField(default=0)

    categories: fields.ManyToManyRelation["Category"] = fields.ManyToManyField(
        "models.Category", related_name="categories"
    )

    thumbnail_url = fields.CharField(max_length=512, null=True)
    thumbnail = fields.CharField(max_length=200, null=True)

    bitrate = fields.CharField(max_length=10, null=True)
    duration = fields.IntField(null=True)

    def __str__(self):
        return self.url

    def get_date(self):
        return humanizeTimeDiff(self.publication_date)

    def get_size_mb(self):
        return f"{self.filesize / 1000 / 1000:.2f} MB"

    def get_size_mb_int(self):
        return self.filesize / 1000 / 1000

    def get_time(self):
        seconds = self.duration or 0
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        remaining_seconds = seconds % 60
        return f"{hours}:{minutes}:{remaining_seconds}"

    class Meta:
        table = "podcast"
