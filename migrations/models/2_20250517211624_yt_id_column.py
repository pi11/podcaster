from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "podcast" ADD "yt_id" VARCHAR(25) NOT NULL UNIQUE;
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_podcast_yt_id_2945ac" ON "podcast" ("yt_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_podcast_yt_id_2945ac";
        ALTER TABLE "podcast" DROP COLUMN "yt_id";"""
