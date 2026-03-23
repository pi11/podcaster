from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "podcast" DROP COLUMN "only_related";
        ALTER TABLE "source" ADD "only_related" BOOL NOT NULL DEFAULT False;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "source" DROP COLUMN "only_related";
        ALTER TABLE "podcast" ADD "only_related" BOOL NOT NULL DEFAULT False;"""


MODELS_STATE = (
    "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"
    "5Uy/8BaTOQtg=="
)
