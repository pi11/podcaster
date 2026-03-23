from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE "podcast_category" (
    "category_id" INT NOT NULL REFERENCES "category" ("id") ON DELETE CASCADE,
    "podcast_id" INT NOT NULL REFERENCES "podcast" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "podcast_category";"""


MODELS_STATE = (
    "eJztW9tu2zgQ/RXBTynQLRJv3Bb7ZifO1tskLhL3ghaBQIu0TUQiVYqqoxb+9yV1pSTLkh"
    "XJufkliUl6ZnjOcIbkMH86FoXIdN70EcPGovOP9qcDbFv8Djs6r7UOARZKWqKhooODqen3"
    "gLgJE4jukCMaf9yIjxYgYI6g+Ehc0xQNYOpwBgwuWmbAdJBosm/1GUYm9JVHujCU0lyCf7"
    "ryM2euHArRDLgmT8QF6mAyQraHVkXy4VQ3qOlaJJELqSHMwGSeSJojghjgqizfKp17tm/R"
    "iPAz30zRY1Aip4EJd3yr53LEX92j43fH7/9+e/xeDPFNiFverXzrHYNhm2NKEr22xxeUxF"
    "qEyE5gc6I90OHbcDnprFbrJzALYUyw71qZFtqlmRYIOFCaEvx/IeZIO1USYkCLWYiGlNGg"
    "iC/hIvp6moyTBWCFbFjgTjcRmXPpz91eryr2QsgG7L/0r04+9K8OhMBXchgVbhx4/2XY1Q"
    "36JEEJkHI1tQRiKLplAI8OD5sFUAgsBNDvSwMojOMoWBVtgKiIrwXkf9fjyyIgq+L2mYje"
    "HxAb/LVmYoffbEBR6pPdluP8NFXwDi7637K4npyPB7LJpg6fM1+KL2AgML4pMi5AWed0jv"
    "gCsShUTIFxuwQM6rlAE/dk4oucfpgzrqnLDFQpvYRD1fTixE379LLz9NIJCHG0A4+63J0i"
    "zVgAQgRVvrc1m3ZcZrZDTCi45VjZazpW9jbEyl4+Vvq/WwqUkey283XTEHY3QNjNQ2hhok"
    "NXzKZ893NYC8esglp4Pp5okU8jJQFjq/SS8JLkgKacuw7ug9DKs49XyIwprJn2w4T3iUID"
    "OBHSiawwuK0qpthITJUcq6iMk6ydtO2z7KM4xD2884s5CX9BPIjh/euT/ulQWsHAMqY7NE"
    "4PSEnDfUYZwnPyEXk+6iMBOCDBRO63ZpJNYuGSSe9DlPOEmOOcMoyces7JF4y684WyZPRQ"
    "pNdpBWy9PCxdAOJNqPyZw9kHTM+s/xPF4KpEzCjzI9At8hQYvZD39TSpeuIQFgqIwAu+z2"
    "Q4RVBfz1Ihyfut5a62ll7EVPMAxqJbvwpq+iZow0XQM9yaP7QLqorvj2TkviqQGQ218Jyg"
    "u8I9RjPwTYbfJpuvgCwv7DkfX/4bDc/eC2Wu2RjyAzCofdMGXE51QpdbOG5aaS24T0Uvxx"
    "YqdGGhAo6J6UVpoyIFMJT7Jvqjo0xRBxCmXGgtTaOL4fWkf/EpxdVpfzKUPd0UT1HrwdvM"
    "goiFaF9Hkw+a/Kh9H18Os7d68bjJ9wyxrg2bI7ZqSkzp3PPaBq+2OzWx4Z9BdTmXHS7bda"
    "pbIblJUpWZPGJWsaOLgzX+VUZn6KLb7xVSCurdgVBqIkDuy9lUiNmQ5Abj8XmKisEom8U+"
    "XwyGVwdHPgdiEA5OTtHxOoWpBB/BEkyjllqgJhpeDKhgCTAX8/Tn3ia2OUUvBmKbUQM5Ts"
    "uuqyp5MdBCuiQmBbBdbNNaXga4M2w2cdRdd0CLRLd+U9B0Eaq3oQjVy5105TQd/LsMxXoF"
    "KFX4Ey8+qZjxhWtNCcCmnr3pa879cjravnE56jZ843LULb5xkX0FmLaN5y7W9AMXllNlkj"
    "ZuAVMKnvjC3unjpLhKUaV0qpY04tqpWgDaF093/0TpC4aIaioLJc+Snks5cC1P21YDldcA"
    "NYuB6Vpe6TOHbCkwU0tsvxaYK8Y0trp2VIp5iEe5a1765Nddzdc9Qg7heBZeKjpNpsjH8s"
    "wnShyj1FQ3evQWuSsjdZtMljcol9d0nBuzT3O7T3MRY1qaDm1JGXRyWS+X47zdL6tKD4gy"
    "4X9HT4jUjVzFR0T3zTJPr+T/4P/8kXaNVv4BJK3i2R2cyqNGc2eq1f+3vCF5"
)
