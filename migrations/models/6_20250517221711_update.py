from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "podcast" ADD "is_active" BOOL NOT NULL DEFAULT False;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "podcast" DROP COLUMN "is_active";"""


MODELS_STATE = (
    "eJztWm1z2jgQ/isef6IzuU5wQ9u5b0DIlGsTOgnt3bST8QhLgKa25FpyKe3w30/yq2zH4D"
    "g2pAmfCLvK7up5pF1pxW/doRDZ7GUfedha6n9rv3XguuIzUugnmk6Ag1JJPFQoOJjZgQYk"
    "Ikwg+omYEH69FV8dQMACQfGV+LYtBGDGuAcsLiRzYDMkRO43c46RDQPnsS8MpTWf4O++/M"
    "49Xw6FaA58m6fmQncwHSHlUVSxfTgzLWr7DkntQmqJMDBZpJYWiCAPcNVWEJXJ124Q0Zjw"
    "iyBMobEokdPAhLMg6oUc8ZfRPXtz9vbV67O3YkgQQiJ5swmiZ5aHXY4pSf26a76kJPEiTO"
    "phzKn30EcQw9VU32zunsA8gjHF3nByEmrQnAQCDhRRiv8P5DEZp0pCAmg5C/GQXTQo5ndw"
    "Ef97lozhEnilbDjgp2kjsuByPRu9XlXshZEt2H/uXw/f9a87wuALOYyKZRyu/qtIZYQ6SV"
    "AKpNxNLYEYmW4ZwO7pabMACoOlAAa6LIAiOI7CXdEGiIr5WkD+czO5KgOyKm6fiNB+hdji"
    "J5qNGb/dgqL0J9UOY99tFbzOZf+/PK7DD5OBFLmU8YUXWAkMDATGt2XBhSibnC4QXyIvTh"
    "UzYH1bAQ+ahUSTaHL5RU4/qhk31PcsVKm8REPV8sIS0bG87L286CEhTOusqc/9GdKsJSBE"
    "UBWstmbLju/Z7RATGW45V/aazpW9LbmyV8yVwWdLiTK23Xa9bhpCYwuERhFCBxMT+mI2u0"
    "8/p7VwzDuohefjyRbFMrIjYdyrvKS8pDWgqcVdB/dBFOXF+2tkJxTWLPtRwftIoQVYjHRq"
    "K0pum4olNjZTpcYqLpMi66ayY5V9FJe4wy9+MSexXhAPc3j/Ztg/H8koPLBK6I6CM0NSsn"
    "BfUA/hBXmP1gHqYwE4IOFEHrZn0kNi6ZY5nkMOdw5Zc7OtvZ+Ybr1v0HTbYEvX4Ame4w69"
    "BC0PyZmYoHbnAPicmoSu7oFt1mkthM+FlmMHlaIsXMAJsddxrqsIMozsvoz/0JUpmgAqW7"
    "CEiOn4cnQz7V9+zLQfzvvTkdQYgXSdk3Ze5zhLjGj/jqfvNPlV+zK5GuW7FMm46Zccsb4L"
    "myO2atbO+Dzy2gavrj+zsRWcqU05lz1u27tct0Jyk6QqM3nErGJmiosC/rGLzlhy/3qW8V"
    "DvUkepjQB5KGkzYWZLHRtMJh8yXAzG01w9+3Q5GF13ugEJYhAOz93xfSEDqkQfwTZBTT08"
    "H1A9aiHGWsZVdfJsoIV0RWwKYLvYZr08D3Dn2G7irpCeEVJEY9OtX7Wabvn2trR8e4Wrgp"
    "wmw792oViv3asa/8NbvSpmfOk7MwKwbeZbJc0tv4KPtq+sXaPhK2vXKL+ySl0W00wjrY2r"
    "f8bBH74Y9/p8PRSgLKi31qs015PBJ0p33VKEx/b6/h+xP2OIqKay0OzDdaFj1xgbe+rXHe"
    "JnPne8HRZ5qvleKOwQjufRtZ49xYfDONGMM1N96DtiidX7ZL5iQIU8aOLCmGNa3H9ajBnT"
    "snRoK+pBVsiSSne9sEH3ta0qPUkqq2yPj5Jq4W/nWfIJvAsd/Oek2aXRyk9Ksy6e3EF7d9"
    "Zo7gy++R+5gZql"
)
