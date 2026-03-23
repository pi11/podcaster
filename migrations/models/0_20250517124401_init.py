from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


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


MODELS_STATE = (
    "eJztWV1v2zYU/SuCnjwgKxovbou92Y6Dem3iInG7oUUg0CItE5VJlaSWGoX/+0jqi5IiW1"
    "EkJwv85Pjy5tzLc8h7SfqXvaYQ+fzVEDHsruw/rV82CAL5GQ/YJ5ZNwBpllsRVDgiw8PUI"
    "SE2YQPQTcWn8diu/rgEBHoLyKwl9XxrAggsGXCEtS+BzJE3Bd2eJkQ918CQWhgotJPhHqL"
    "4LFipXiJYg9EUGF4WDmYeyx1kl+HDhuNQP1yTDhdSVaWDiZUgeIogBYWLprByxCXRGUyIu"
    "dJpyxKVETQMTwXXWnvL4vX969vbs3R9vzt5JF51Canm71dlzl+FAYEqyuMFGrChJo0hIO8"
    "o5ix7F0Dlcze3t9v4JLGMaM+7764KF9mnBAoEAhinj/1/EuMrTFCEltFqFxGWfDAb8Hi2S"
    "f8+LMV4BVqnGGvx0fEQ8odZzfzCoy70E2cH9l+H1+P3wuicBf1NuVC7jaPVfxUP9aEwJlB"
    "GpdlNHJMbQHRN4+vp1uwRKwEoC9VieQJmcQNGu6IJEA74RkX/dzK6qiKzL22ciR79B7IoT"
    "y8dc3O5gUcVTw2vOf/gmeb3L4T9FXscfZyNlCigXHtMoGmAkOb6tSi5i2RHUQ2KFWFIqFs"
    "D9fgcYdEqFJh0p1Bc1/bhn3NCQuahWe4ldzfbCU9OxvRy8vdiRINzqbWgowgWy3BUgREql"
    "V1u7bSdkfjfCxMAd18pB27VysKNWDsq1Un92VCgT7K77ddsU9ndQ2I8oLJfCPYv+QSUyky"
    "erY20J1ESLUZzlxYdr5AMRH8Matq64aH+i0AU8qS0ZVrxBtzXbRAJTp08YIdNGEWS2Y6d4"
    "FheRp1/8ck5yvSAR1aHhzXh4PlFZMHCXyh0n50Si5Om+oAxhj3xAG836VBIOSDSRx+2Z7K"
    "BTuWWOvfTYS//HFLoMqZk4oPHtDYSCOoTePYDbfNBGDJ/LUYHXqJJlGQLOiL9J9mpNkmGM"
    "+yr5wzam6ABo7MEKIebTy8nNfHj5KXcFPB/OJ2qkr62bgrX3pqBZCmL9PZ2/t9RX6+vsal"
    "K8KaZ+868FYcMAtids3aqTi3nUtQtdg3DhY1efCR01lwNu2/tCdyJym6IaM3nGqmLuKEcE"
    "98iZWB7ez3IRml1KKPURII8VbSFhdvSx0Wz2MafFaDov9LPPl6PJde9UiyCdcHRuTM67xe"
    "Osg/eR2viMkAvQiNPnc1E46FvjWJLiUbax69wiU+cT4xrpGsbjPfLwL45fMETUMlVo95Wx"
    "dLRvTY0DHeyf4jeZex7Jyjo1fBiTOETgZdz/+Ut8IUsKzTQ31cc+mFWgPqTylRMq1UEHl3"
    "yOZfHwZTFRzMrLYd1RBnmpShrX8NIGPdS2qvX2ZqyyA76+mY2/m/e3F/CA9OS//eeXRie/"
    "/+dDvLiD9v6q0d4ZfPsf1NZRqQ=="
)
