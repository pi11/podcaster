from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "podcast" ALTER COLUMN "source_id" DROP NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "podcast" ALTER COLUMN "source_id" SET NOT NULL;"""


MODELS_STATE = (
    "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"
)
