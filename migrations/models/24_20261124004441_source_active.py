from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return 'ALTER TABLE "source" ADD "is_active" BOOLEAN NOT NULL DEFAULT TRUE;'


async def downgrade(db: BaseDBAsyncClient) -> str:
    return 'ALTER TABLE "source" DROP COLUMN "is_active";'


MODELS_STATE = (
    "eJztXF9z2jgQ/yoentKZtBNIaTv3Bkl6zbUJncTXdnpz4xG2MJoYidpyEq7Hdz/J/y3Jxi"
    "aBAqeXNki7svzb1e5qtdbPzow40AteDQHG0PlKfCfo/Gb87GAwg+wPVfex0QHzed7JGygY"
    "exH9OCK0HjLKcUB9YFPWNwFeAFmTAwPbR3OKCOYc8dBGxuEQm7Eg7Ko6Q4x+hNCixIV0Cn"
    "1G8tffrBlhBz7CIP05v7MmCHpO6U2QwweI2i26mEdtl5i+jwj5c8eWTbxwhnPi+YJOCc6o"
    "Eaa81YUY+oBCPjz1Q/5KOPS8BIH0LeOZ5iTxFAs8DpyA0OPAcO54Anlbx7KuR6Z1e2FaVk"
    "cCLeUoQJU02QRzwNlUYzm6fAove93Xb1+/O33z+h0jiaaZtbxdxo/OgYkZI3iuzc4y6gcU"
    "xBQRxjmo0f8SrGdT4KtxTekFZNmURWRTHOugTRtybHMd2wa4M/BoeRC7dMp+dk9OaqD8Mr"
    "g5+zC4OWJUL/gjCVsU8Yq5Trp6cd9yyTV4cleAmzeMgX33AHzHknpIj1TRyl2z3kxsARi4"
    "EXb8JfkbJEv+jAnCJf5CZQ6yvlpbYBepVtqBL8iBxCjylCyB3K1tgbYFuwLtL7cERd2GmK"
    "IJYkuFvUUgS2SYDPD+4w30IiKFFISFflkadA9t9TLVvrQ10ZDlE01ojntimhBUQH4F8MIk"
    "/N9oKVyySQBsq7Q/wf0zcWwQSCZm5xdCFcypW7EER1J4T58rIwsdK/AkfiSPO8gdUmce81"
    "mxbc6klfSmXiLpplOfhO60yFf0Iwx9NhdIY3M1uD0bnF/wdks07stG/lJYKjXeU15Uq32p"
    "hWSmla41faBRZq6IuVdSa8erHe/OGPYNud5jQ7LsqTlpqL0C12o13gewn0GTpaBGBlpG+T"
    "3xIXLxR9jUgRZ3KHsGco0P9cFDZlRFBVO6seWv2Tumbl3h/Aoev9rbzQtEq7xbNa7aT+2W"
    "nwp9r42bSsgPbnvYb+Sj+jU+qi/7qAVVeqdqdDOGg8O3128Ab69fiS7vKoOrA6zNKm9xZh"
    "LMJnyssLsC21poJ2q6K2DXYGtefDP5yLMg+OEVIT26GnyL0J4tkp5Po+vfU/KCCM4+jYZi"
    "aOvDaNMNqAz8OeuhaAYrwtsSp4C9k7C+Sv/YR71nL+iMsLdItKRONJdXF7fm4OpzST7nA/"
    "OC9/RKsklbj94IKyQbxPh6aX4w+E/j++g6SkXMSUBdP3piTmd+7/A5gZASC5MHCzgFu5u2"
    "pqiVpB7OnTWlXubUUt8VqacYFcSezD6X+jwce0kux+ISait7Ff8BasD+Slxe6Ciw2NYJ3S"
    "tkPSTEgwBX7GiKfIKMx4xxU2JNg8btinU4Gn0qSXR4KbrOP6+GFzdH3UiUjAjFu+x0y1MC"
    "nMsQKkLxVYDnfFsEPGvZZ8TBA0CUzSSCcA1NF9k1/i013ic2DIK1lL7IqnFvh7tDHrBHgL"
    "MO8GVejXwL5CfIa5UNSOkPYX8qZlqaJAMYVU2uRUoGcLgC9I8C4soEbJFle+csJ5vC+FnS"
    "sDmgdBrOxhggz2qZgJUYD0+D+91ek3RWt1edzuJ9FYCvBfZhAt1rlDfs1eQNe3LecIyor9"
    "zIVsNcYDk8kLvNDr9rzr6lzGzoA3VattIYF1nWMsa7BvEzm+MJW+OQkaGZqlKs2scJbNrP"
    "icAGJPRt2K5Io8SjtVURPLiWPeUfYXjtgJX4NLgry19iZZRBbl38cpsNtF/4Nq18Ka1add"
    "2LWoefAVvTPcvHOkx4pbW75dKiDdVUP6UkbK+Kqosv2qqqWqgoE8uqy0XXz1FVHZ9Y1JeS"
    "+eRR+Q1S3HFcW0aWkawskf5gmp+NiN4IA+gY44WxoC8db24A7BjZ5sxI82bBq44guzWH0E"
    "VqukhtN4DdTJ3PjnzNmIRECjuSB0vVhiSPzFZbkni8wDhakJCGY2gkvjR4IVmMelJtGbRl"
    "2A1gN18BqCssN5sp1YUgWz4knCEW/7ZPnopsOssnAcvWyjrACmzbA7Z78u5kX8Al2FtYyZ"
    "axpaUQWXVJQRtrwbTznl9wEVhz6Fdnq2rVWz3AFhW9vydaDh+jEN6iwFVdj1Cn5SKr1vIW"
    "Wq7PErZ3lqBz3lvOea8+xmlz70rz+z/2BO+n3rNSm9zJ9VOR3ykpb3WKh7qF9aI/Ot4rO3"
    "hck7XRmYXNXo7BDGe7D48zhoPLjJ02gfe0Gt1TCdzo4541vmoo8ekYdUWM2uKIoqj3lfHV"
    "/9vRN628aIPSoRW0bDQaGkAf2VNVKJT01MZBIKfRQdChBEH30A+U+dJqN11gOcBQqNdvdk"
    "lI3S0h0jUhfFG1QDghP0B0N3MLG8EUYkUk9Mft6FqNcIFF/FAd2dT41/DQends7oZbUYHL"
    "wSiFQtItIeKFIMflz875AMNfXbex/A88Lldh"
)
