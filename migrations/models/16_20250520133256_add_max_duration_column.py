from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "source" ADD "max_duration" INT NOT NULL DEFAULT 10800;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "source" DROP COLUMN "max_duration";"""


MODELS_STATE = (
    "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"
)
