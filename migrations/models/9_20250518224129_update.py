from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "podcast" ADD "is_awaiting_post" BOOL NOT NULL DEFAULT False;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "podcast" DROP COLUMN "is_awaiting_post";"""


MODELS_STATE = (
    "eJztWm1z2jgQ/isef+Jmcp3gC23nvgEhV65J6CS012kn4xGWAE1tybXlEtrhv5/kV9nm1b"
    "EgDXxKWam7q+dZ7Vor/dIdCpHtv2ojD1tT/W/tlw5cl/+NB/QzTSfAQZkkmcoHGBjZ4QhI"
    "RZhA9Ih8Lvz6wH86gIAJgvwnCWybC8DIZx6wGJeMge0jLnK/mWOMbBgaT2xhKLQFBH8PxG"
    "/mBWIqRGMQ2CxTF5mD2Qwhj71K9MORaVE7cEimF1KLu4HJJNM0QQR5gMm6Qq9MNndDj/qE"
    "XYVu8hGLErEMTJgfej0RM/40mhdvLt7+9friLZ8SupBK3ixC733Lwy7DlGR23TmbUpJa4S"
    "r1yOfMemQj9OF2qC8WyxcwjmHMsDecgoQatCCBgAFJlOH/A3m+8FMmIQV0NQvJlE00SOo3"
    "cJH89zwZ3SnwVrLhgEfTRmTCRDwbrda22HMla7D/1L7rvmvfNbjCP8Q0ysM4iv7beMiIxg"
    "RBGZBiNykCMVatGMDm+Xm9AHKFKwEMx/IAcucYinaFChAl9ZWA/Pd+cLsKyG1x+0j46FeI"
    "LXam2dhnD2tQFPbEsOP7320ZvMZN+3MR1+71oCNELvXZxAu1hAo6HOOHVc5FKJuMThCbIi"
    "9JFSNgfZsBD5qlRJOOFPKLWH5cM+5p4Floq/IST5XLi5+KTuVl7+VFjwjxtcacBiwYIc2a"
    "AkI4VWG01Vt2As9WQ0ysWHGubNWdK1trcmWrnCvDv4oSZaJbdb2uG0JjDYRGGUIHExMGfD"
    "Wbv37OK+FYNFAJz+eTLcplZEPC2Km8ZLxkNaCu4K6Ceyf28ur9HbJTCiuW/bjgfaDQAn6C"
    "dKYrTm6LLUtsomabGiuZTIusm8lOVfZZHOIOH/x8TTxeEItyePu+277sCS88MEvpjp0zI1"
    "LycF9RD+EJeY/mIep9Djgg0UKetmeyj8SVW+b0HXK475A5M1Xt/VS18r5B3W2DNV2DF/gd"
    "d+gQlA0/HckkfGUgCxYq4TlEjysLUj3wDXufh+v7Bc48Hrke3P6TTC82EQo9GQ+JZZmgcl"
    "sGBIyahM52CNy80UpwX/JRhh20MoS5CTgg9jwpJFtSAGO9r5J/6NISTQBhLoSW0tS/6d0P"
    "2zcfclxdtoc9MWLkeEqkjdeFDZEq0f7rD99p4qf2ZXDbK7aA0nnDLwViAxfWR+y2JTFn88"
    "SrCl7dYGRjKzywmGIte9y2y0wrIblOUqWVPGNWsW/yUxj+sYnOOER3/1bIGah2YKbURoA8"
    "lbMRV7OmyHUGg+scFZ1+sYp9vOn07hrNkAM+CUdnmuQslsNUgI/gBkwTSSVQMwtHAyqYAc"
    "z4OsO1q8S2ZOhoIHY9aiHfVxy6spGjgRbSGbEpgGqxzVs5DnDH2K7jqLvsgJaoVt4pqPvG"
    "orXmxqJVOumKZfr45yYUq91WyMp/85sKGTM2DZwRAdg2i52++sKvZEN1x6Vp1NxxaRqrOy"
    "5ibAWmqvE8glvIXE9dRRcwZ+A339h7fcnS5aBMqDfXt7lnSyefSRdtliQ83bTt/z3LJwwR"
    "1WQW6n3DUmre18bGnlr3h3jxt+QZQZmnik8HuB7C8DhuQvn7v0ZV/4YgSTT93FLX3o/ukO"
    "sKWnfJfGWHSnnQxKU5p7S4/7SYMKbl6dBm1IN+KUtKd0GlDbqvbbXV6wQpyvQSG8reJ8iF"
    "X80LhRdwRXzwl+X50FDyujxv4sV9aG/OGvV9gy/+B3VA5nY="
)
