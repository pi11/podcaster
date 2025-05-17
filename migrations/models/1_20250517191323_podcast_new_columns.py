from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "podcast" ADD "filesize" INT NOT NULL;
        ALTER TABLE "podcast" ADD "file" VARCHAR(250);
        ALTER TABLE "podcast" ADD "is_processed" BOOL NOT NULL DEFAULT False;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "podcast" DROP COLUMN "filesize";
        ALTER TABLE "podcast" DROP COLUMN "file";
        ALTER TABLE "podcast" DROP COLUMN "is_processed";"""
