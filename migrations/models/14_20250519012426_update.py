from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "source" ADD "max_videos_per_channel" INT NOT NULL DEFAULT 15;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "source" DROP COLUMN "max_videos_per_channel";"""


MODELS_STATE = (
    "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"
)
