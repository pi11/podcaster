from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "source" ADD "max_duration" INT NOT NULL DEFAULT 10800;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "source" DROP COLUMN "max_duration";"""
