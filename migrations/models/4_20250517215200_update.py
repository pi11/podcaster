from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "podcast" ADD "thumbnail_url" VARCHAR(512);
        ALTER TABLE "podcast" ALTER COLUMN "filesize" SET DEFAULT 0;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "podcast" DROP COLUMN "thumbnail_url";
        ALTER TABLE "podcast" ALTER COLUMN "filesize" DROP DEFAULT;"""
