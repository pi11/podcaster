from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "banned_words" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL
);
COMMENT ON TABLE "banned_words" IS 'Banned words';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "banned_words";"""


MODELS_STATE = (
    "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"
    "xDy385ybLYu0LD6l2jOr/09D8cgDEs"
)
