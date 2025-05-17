from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "podcast" ADD "description" TEXT;
        ALTER TABLE "podcast" ALTER COLUMN "is_active" SET DEFAULT True;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "podcast" DROP COLUMN "description";
        ALTER TABLE "podcast" ALTER COLUMN "is_active" SET DEFAULT False;"""
