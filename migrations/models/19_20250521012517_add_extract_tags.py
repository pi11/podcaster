from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "source" ADD "extract_tags" BOOL NOT NULL DEFAULT False;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "source" DROP COLUMN "extract_tags";"""


MODELS_STATE = (
    "eJztXFtz2jgU/isMT9mZbieQ0Gb2DQjZZtuETkIv007GI2xhNDESteUQt5P/vpJ8k2Uuxl"
    "gkAV6SIIlzpO8c6ehclD/1CbGg471tQxeZ4/o/tT91MJ2y31FH/U2tjsEEpi3xUNZBwdAR"
    "PSBpQtiCj9BjjT/v2McJwMCGFvuIfcdhDWDoUReYlLWMgONB1jS9N0YIOpZgHvNCFqfmY/"
    "TL55+p6/OhFhwB36EpuZCdlY7g7dGsYvrW0DCJ409wStciJpsGwnZKyYYYuoDKtMSsDBpM"
    "xYwuMb0Q02Q9JsF8GQhTT8za5iP+bjZO35+enbw7PWNDxBSSlvdPYvae6aIpRQSnfKcBHR"
    "OccGEk6+GcU+4hDzGH60H96Wn+AkYRjCn2zYnSQppEabEABVJTiv8DdD0+T1kICaCLpRAP"
    "WSUGifwKWcRfzwqjOwbuQmlMwKPhQGxTrs/NVqso9ozIEuy/tm+6H9o3R4zgX3wYYWocav"
    "911NUM+7iAUiD5btIEYkRaM4CN4+NqAWQEFwIo+rIAsslRGO4KHSBK5EsB+d9t/3oRkEVx"
    "+4JZ708LmfRNzUEevVuCIufHuyee98uRwTu6an9Xce1+6nd405R41HYFFUGgwzC+WzS5EG"
    "WDEhvSMXTjo2IIzPsZcC0jd9AkPcr5wpcf2Yxb4rsmLGReoqGyefGSpoN52bp5qYcC8WpH"
    "AfGpP4Q1cwwwZqIS2pbRhhRgahvRsAo2biyeYvuTLZcpEqThOde+7bbPe3wSLpglmiDNzw"
    "hllpXGBXEhsvFHGAihXDJ5AByqYMk9Hmn3wO6msAjVialF63za2HT7rqNHuSPCmu1Nq2p7"
    "01pib1p5eyN+azI2MW3dd56qIWwugbCZh3CC2Bb02WpW3yCPS+GoMiiF50s6cSXsmCALYt"
    "c4PjsuiZ/CZIfwI9gJDBc6YurL8Ytb1sdPZVIKvw4hDgR408vjkJFZglCn3/+UuS92LgfK"
    "Vv5y1emxa7nY4WwQCi3nfNV8QBYknjGFbkH73miV1tD5vHZIV+GjuKwaFNieNl1VmeyHru"
    "budxVdQWVkczxeuWrmPcIVd/+1PMVUNqk7V9Udq5RKR7O8+HjDD/LIEm52u/9MLBN4MdLz"
    "7/YFvOWYTBF3WWKZ+MvTtO3gML+IeOzzK38hrzic3HY94jTeU9AdlkKDbI02cRH0yiknHb"
    "vEt8fSljEikkFdC9jG6mPpCuBgQPjPHM4CMEPZ/11pwkUFMSKuOIHuYSDBGERyny8mmU9y"
    "hEUEYvDC70f3YmO+lBYK+RDh2FaEI6DqnagyABPS2rM6VSd1luR0djBC9NwqKDPWczlXOJ"
    "TCc8B8p01dnuXwDXrfB8uzOZMg6vnUv/43Hq6meJSMmQvFAQxKJ82AT4mByWwNxc0yLQX3"
    "OeulaAIXqjBjYfWxE8Rmo6AIrIju2/iPurREA1hWRoXmiunyqnc7aF99zsjqvD3o8Z5mRk"
    "5x69E7ZUMkRGrfLgcfavxj7Uf/uqcm6JJxgx+KYP2pVZ1gi5rEDM+DXHXIdeoPHWQKH9Tg"
    "a9nitp3HWouQqxSqtJIXLFXkGcyxRg+rxBmp6Pp3hQyD/QjrsSVz8DWG9jMc9gZUMAOIsn"
    "WKtevENsdobyCeusSEnqdZdWUmewOtRWbYIcDSi22Wy36AO0JOFa7uPActJq09UlB1LURr"
    "SS1EK+fp8mV66PcqFMvl8WXirzz5lEnejf3JEAPkGGqkr8LkncpDd8Sl0aw44tJoLo648L"
    "4FmOrGcxt7+pnrm4aIuhu4aSuQlKhrL+2uurJ7SWF3LgRYrMipdPxvN8ubMhk6HQHoDINX"
    "DtxWS9yTBFmRrL2cTUvS9nLu8ZC3336h+1deb1aTpbDiTdWuZKLnymndRLRUiFIyD51NI6"
    "+ssFGz0EoaW38aOpcHrGx3bSkL+BxPu+YUmeX3XcnCMkYHUzSK4tmrSipfZYVZbDguM0td"
    "qtEFbFf6KqWI8cq8YUmsF7WlIt2D+XoRZWcbvyXagVKH536/Sm1t1TYJac0QnlSM4MliAE"
    "9y+Incn9a0RIbD7sZ1q/GGXsQTT/12tkBVagG72uHwWN+Ia3mFLKs8XratQ9FuzOKOg3nd"
    "vncYyqaWyOBgaF+AoZ3jTahy0hnrUW7h60R+8hf4XBzIQLkxh42//Y0fS6yWFceCkyAXEw"
    "qq3NYVvvVQwiVbeu0hBz71/PuDw0m6scuiqIaWf7uTZbFziYbVp0Z1dunpf6T7AlE="
)
