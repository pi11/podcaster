from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "source" ADD "tg_channel_id" INT;
        CREATE TABLE IF NOT EXISTS "tgchannel" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL,
    "tg_id" VARCHAR(30) NOT NULL UNIQUE,
    "auto_post" BOOL NOT NULL DEFAULT False
);
        ALTER TABLE "source" ADD CONSTRAINT "fk_source_tgchanne_4ddcfe37" FOREIGN KEY ("tg_channel_id") REFERENCES "tgchannel" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "source" DROP CONSTRAINT IF EXISTS "fk_source_tgchanne_4ddcfe37";
        ALTER TABLE "source" DROP COLUMN "tg_channel_id";
        DROP TABLE IF EXISTS "tgchannel";"""


MODELS_STATE = (
    "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"
    "+dadU0tHxvWmXx4hKSm2+N+nKVi/8BsLe+/A=="
)
