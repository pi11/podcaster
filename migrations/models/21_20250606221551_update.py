from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "podcast" ADD "tg_channel_id" INT;
        ALTER TABLE "podcast" ADD CONSTRAINT "fk_podcast_tgchanne_d12a31da" FOREIGN KEY ("tg_channel_id") REFERENCES "tgchannel" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "podcast" DROP CONSTRAINT IF EXISTS "fk_podcast_tgchanne_d12a31da";
        ALTER TABLE "podcast" DROP COLUMN "tg_channel_id";"""
