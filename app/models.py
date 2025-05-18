"""Models for gmp project"""

import os
import random
from datetime import datetime, timedelta
from enum import IntEnum
from typing import List
from slugify import slugify
from tortoise import fields, models

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


class Source(models.Model):
    """Sources (youtube channels)"""

    id = fields.IntField(pk=True)
    url = fields.CharField(max_length=500, unique=True)
    name = fields.CharField(max_length=200)
    min_duration = fields.IntField(default=0)

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

    source = fields.ForeignKeyField("models.Source", related_name="source")
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    publication_date = fields.DatetimeField()
    is_active = fields.BooleanField(default=True)
    is_posted = fields.BooleanField(default=False)
    is_processed = fields.BooleanField(default=False)
    is_downloaded = fields.BooleanField(default=False)

    file = fields.CharField(max_length=250, null=True)
    filesize = fields.IntField(default=0)

    thumbnail_url = fields.CharField(max_length=512, null=True)
    thumbnail = fields.CharField(max_length=200, null=True)

    def __str__(self):
        return self.url

    class Meta:
        table = "podcast"
