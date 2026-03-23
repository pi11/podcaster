from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "podcast" ADD "failed_times" INT NOT NULL DEFAULT 0;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "podcast" DROP COLUMN "failed_times";"""


MODELS_STATE = (
    "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"
)
