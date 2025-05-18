from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "source" ADD "max_videos_per_channel" INT NOT NULL DEFAULT 15;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "source" DROP COLUMN "max_videos_per_channel";"""
