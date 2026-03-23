from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "podcast" ADD "tg_channel_id" INT;
        ALTER TABLE "podcast" ADD CONSTRAINT "fk_podcast_tgchanne_d12a31da" FOREIGN KEY ("tg_channel_id") REFERENCES "tgchannel" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "podcast" DROP CONSTRAINT IF EXISTS "fk_podcast_tgchanne_d12a31da";
        ALTER TABLE "podcast" DROP COLUMN "tg_channel_id";"""


MODELS_STATE = (
    "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"
)
