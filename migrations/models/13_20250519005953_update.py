from tortoise import BaseDBAsyncClient


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
