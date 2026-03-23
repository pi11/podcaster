from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "podcast" ADD "only_related" BOOL NOT NULL DEFAULT False;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "podcast" DROP COLUMN "only_related";"""


MODELS_STATE = (
    "eJztW9tu2zgQ/RXBTynQLRJv3Bb7ZifO1tskLhL3ghaBQIu0TUQiVZGqoxb+9yV1pSTLkh"
    "XJufkliUl6ZnjOcIbkMH86FoXIZG/6yMHGovOP9qcDbFv8Djs6r7UOARZKWqKhooODqen3"
    "gLgJE4juEBONP27ERwsQMEdQfCSuaYoGMGXcAQYXLTNgMiSa7Ft9hpEJfeWRLgylNJfgn6"
    "78zB1XDoVoBlyTJ+ICdTAZIdtDqyL5cKob1HQtksiF1BBmYDJPJM0RQQ7gqizfKp17tm/R"
    "iPAz30zRY1Aip4EJZ77Vcznir+7R8bvj93+/PX4vhvgmxC3vVr71zHCwzTEliV7b4wtKYi"
    "1CZCewOdEe6PBtuJx0Vqv1E5iFMCbYd61MC+3STAsEHChNCf6/kMOknSoJMaDFLERDymhQ"
    "xJdwEX09TcbJAjiFbFjgTjcRmXPpz91eryr2QsgG7L/0r04+9K8OhMBXchgVbhx4/2XY1Q"
    "36JEEJkHI1tQRiKLplAI8OD5sFUAgsBNDvSwMojOMoWBVtgKiIrwXkf9fjyyIgq+L2mYje"
    "HxAb/LVmYsZvNqAo9clui7GfpgrewUX/WxbXk/PxQDbZlPG540vxBQwExjdFxgUo65zOEV"
    "8gJwoVU2DcLoED9VygiXsy8UVOP8wZ19R1DFQpvYRD1fTC4qZ9etl5eukEhDDtwKMud6dI"
    "MxaAEEGV723Nph3XMdshJhTccqzsNR0rextiZS8fK/3fLQXKSHbb+bppCLsbIOzmIbQw0a"
    "ErZlO++zmshWNWQS08H0+0yKeRkoCxVXpJeElyQFPOXQf3QWjl2ccrZMYU1kz7YcL7RKEB"
    "WIR0IisMbquKKTYSUyXHKirjJGsnbfss+ygOcQ/v/GJOwl8QD2J4//qkfzqUVjhgGdMdGq"
    "cHpKThPqMOwnPyEXk+6iMBOCDBRO63ZpJNYuGSSe9DlPOEmOOcOhixes7JFw515wtlyeih"
    "SK/TCth6eVi6AMSbUPkzh7MPmJ5Z/yeKwVWJmFHHj0C3yFNg9ELe19Ok6olDWCggAi/4vi"
    "PDKYL6epYKSd5vLXe1tfQippoHMBbd+lVQ0zdBGy6CnuHW/KFdUFV8fyQj91WBzGiohecE"
    "3RXuMZqBbzL8Ntl8BWR5Yc/5+PLfaHj2XihzzeYgPwCD2jdtwOVUJ3S5heOmldaC+1T0cm"
    "yhQhcWKuCYmF6UNipSAEO5b6I/OsoUdQBhyoXW0jS6GF5P+hefUlyd9idD2dNN8RS1HrzN"
    "LIhYiPZ1NPmgyY/a9/HlMHurF4+bfM8Q69qwOWKrpsSUzj2vbfBqu1MTG/4ZVJdz2eGyXa"
    "e6FZKbJFWZySNmFTNdHKzxrzI6Qxfdfq+QUlDvDoRSEwFyX86mQsyGJDcYj89TVAxG2Sz2"
    "+WIwvDo48jkQg3BwcoqO1ylMJfgIlmAatdQCNdHwYkAFS4C5mKc/9zaxzSl6MRDbDjUQYy"
    "27rqrkxUAL6ZKYFMB2sU1reRngzrDZxFF33QEtEt36TUHTRajehiJUL3fSldNk+HcZivUK"
    "UKrwJ158UjHjC9eaEoBNPXvT15z75XS0feNy1G34xuWoW3zjIvsKMG0bz12s6QcuLFNxVt"
    "XDa+7WMk5WyctIOKkKVBsXrCkFTzxm7vTdV1wAqlKVVqtFcVlara3t69K7f/31BUNENZWF"
    "khdfz6XSupanbQutykOLmnXWdJm09AVJtsqaKdO2X2bN1bkaW107qnI9xHvnNY+o8uuu5s"
    "MpIYdwPAvva1mTKfKxvKCKEscoNdWNHr1F7spI3SaT5Q3K5TUd58bs09zu01zEmJamQ1tS"
    "B7Jc1svlOG/3y6rS26xM+N/R6yx1I1fxfdZ9s8zTe03x4P9Xk3aNVv63Jq3i2R2cyqNGc2"
    "eq1f/kf5C2"
)
