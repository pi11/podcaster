from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "podcast" ADD "duration" INT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "podcast" DROP COLUMN "duration";"""


MODELS_STATE = (
    "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"
)
