from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "podcast" ADD "is_downloaded" BOOL NOT NULL DEFAULT False;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "podcast" DROP COLUMN "is_downloaded";"""


MODELS_STATE = (
    "eJztWm1z2jgQ/isef8rN5DrBF9rOfQNCplyb0Enoy7ST8QhLgKay5FryUa7Dfz/Jr7IdA3"
    "FsSFM+EXaV3dXzSLvSip+myyAi/EUP+dhZmH8bP03gefIzVpinhkmBizJJMlQqBJiSUANS"
    "EaYQ/UBcCr/eya8uoGCOoPxKA0KkAEy58IEjpGQGCEdS5H2zZxgRGDpPfGGorAUUfw/Ud+"
    "EHaihEMxAQkZmL3MFshJLHUSX24dR2GAlcmtmFzJFhYDrPLM0RRT4Quq0wKlusvDCiERWX"
    "YZhS4zCqpoGp4GHUczXiT6tz/ur89V8vz1/LIWEIqeTVOoyeOz72BGY08+utxILR1Is0aU"
    "YxZ94jH2EM1xNzvb5/ArMYxgx7yy1ImMUKEggE0EQZ/v8in6s4dRJSQKtZSIZso0Ezv4WL"
    "5N/zZAwWwK9kwwU/bILoXKj1bHW7u2IvjWzA/mPvZvCmd3MiDf6hhjG5jKPVfx2rrEinCM"
    "qAVLupJRBj0y0D2Dk7axZAabASwFCXB1AGJ1C0K9oAUTNfC8h/bsfXVUDuitsHKrVfIXbE"
    "qUEwF3cbUFT+lNrl/DvRwTu56n0u4jp4N+4rkce4mPuhldBAX2J8VxVchLIt2ByJBfKTVD"
    "EFzrcl8KFdSjSpppBf1PTjmnHLAt9BO5WXeKheXngqOpaXvZcXMyKEGycrFohgigxnASiV"
    "VIWrrdmyE/ikHWJiwy3nym7TubK7IVd2y7ky/GwpUSa2267XTUNobYDQKkPoYmrDQM5m++"
    "nnrBaORQe18Hw62aJcRrYkjAeVl4yXrAY0tbjr4N6Po7x8e4NISmHNsh8XvPcMOoAnSGe2"
    "4uS23rHEJmZ2qbGay7TIepnsWGWfxCXu8ItfzkmuFySiHN67HfQuhioKHyxTuuPg7IiUPN"
    "yXzEd4Tt+iVYj6SAIOaDSRx+2Z7JBYuWWO55DDnUNWwm5r76emW+8bNN022NA1eIbnuEMv"
    "QcdHaiY2qN05AIFgNmXLB2Cbd1oL4QupFdhFlShLF3BMySrJdTuCDGO7L5I/TG2KNoDaFq"
    "wgYjK6Gt5Oelfvc+2Hi95kqDRWKF0VpCcvC5ylRoxPo8kbQ301voyvh8UuRTpu8qVAbODB"
    "5ojdNWvnfB55bYNXL5gS7IRnalvNZY/b9j7XrZDcJKnaTJ4wq5jbaiCCW+hMJA+vZzkP9S"
    "51jBEE6GNJm0ozG+pYfzx+l+OiP5oU6tmHq/7w5qQTkiAH4ejcndwX8qD6TF6xecu46k5+"
    "G2ghW1LCAGwX27yX3wPcGSZNHGuzcpYhmphu/VbQdHeyu6E72S2datU0Of5vG4r1OpO68V"
    "+8K6ljJhaBO6UAE7t4q29u+ZV8tH276lgN3646VvXtSunymOZ6Pm3cUnMOfvHFuNeX1oEE"
    "Zc78lblLHzgdfKo1gh1NeOwE7/+99SOGiBk6C82+sZaaS42xsafW0iF+kXLPM1eZp5pPW9"
    "IOFXgW30D5c3zjShLNKDfVxz55VVh9SOYrB1TKgzYujTmmxf2nxYQxI0+HsWQ+5KUsqTWC"
    "Sxt0X9tqp9czbZXt8f1ML/ztvKA9gyeMg//yMb80Wvn1Y97Fsztob88azZ3B1/8DPJ4t/g"
    "=="
)
