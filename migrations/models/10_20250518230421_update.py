from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE "podcast_category" (
    "category_id" INT NOT NULL REFERENCES "category" ("id") ON DELETE CASCADE,
    "podcast_id" INT NOT NULL REFERENCES "podcast" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "podcast_category";"""
