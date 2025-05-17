from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "category" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL UNIQUE
);
COMMENT ON TABLE "category" IS 'Video category';
CREATE TABLE IF NOT EXISTS "category_identification" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL,
    "category_id" INT NOT NULL REFERENCES "category" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "category_identification" IS 'Category identification words';
CREATE TABLE IF NOT EXISTS "source" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "url" VARCHAR(500) NOT NULL UNIQUE,
    "name" VARCHAR(200) NOT NULL
);
COMMENT ON TABLE "source" IS 'Sources (youtube channels)';
CREATE TABLE IF NOT EXISTS "podcast" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "url" VARCHAR(500) NOT NULL UNIQUE,
    "name" VARCHAR(500) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "publication_date" TIMESTAMPTZ NOT NULL,
    "is_posted" BOOL NOT NULL DEFAULT False,
    "source_id" INT NOT NULL REFERENCES "source" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
