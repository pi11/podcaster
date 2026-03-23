from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "podcast" ADD "yt_id" VARCHAR(25) NOT NULL UNIQUE;
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_podcast_yt_id_2945ac" ON "podcast" ("yt_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_podcast_yt_id_2945ac";
        ALTER TABLE "podcast" DROP COLUMN "yt_id";"""


MODELS_STATE = (
    "eJztWltz2jgU/iseP7Ez2U7Dhrazb0DIlG0TOgm9TDsZj7CE0dRIriRvynb47yvJN9mOwS"
    "E2ZLM8EY6U7xx9n3SOLvyylxQin7/oI4bdhf2n9csGQSA/4wb7xLIJWKLMknSVDQLMfN0C"
    "UhMmEP1EXBq/3cqvS0CAh6D8SkLflwYw44IBV0jLHPgcSVPw3Zlj5EPtPPGFoUILCf4Rqu"
    "+ChaorRHMQ+iKDi9zBrIeyx1El+HDmuNQPlyTDhdSVYWDiZUgeIogBYWLpqByxCnREYyIu"
    "dJiyxaVEDQMTwXXUnurxe/f07PXZmz9enb2RXXQIqeX1WkfPXYYDgSnJ/AYrsaAk9SIh7S"
    "jmzHvkQ8dwNbXX6/sHMI9pzLjvLgsW2qUFCwQCGKaM/78R4ypOU4SU0GoVki7bZDDgt2iR"
    "/HtejOECsEo1luCn4yPiCTWfu71eXe4lyAbuP/Wvh2/71x0J+JvqRuU0jmb/VdzUjdqUQB"
    "mRajW1RGIM3TKBpy9fNkugBKwkULflCZTBCRStijZINOB3IvKvm8lVFZF1eftIZOs3iF1x"
    "YvmYi9sNLCp/qnnJ+Q/fJK9z2f9S5HX4fjJQpoBy4TGNogEGkuPbquAilh1BPSQWiCWpYg"
    "bc73eAQaeUaNKWQn5Rw49rxg0NmYtqlZe4q1leeGo6lpe9lxc7EoRbnRUNRThDlrsAhEip"
    "9GxrtuyEzG9HmBi45VzZazpX9jbkyl45V+rPlhJlgt12vW6awu4GCrsRheVUuGXSPyhFZv"
    "JkeawpgXbRYhBHefHuGvlAxNuwHUtXnLQ/UOgCnuSWDCteoOuaZSKBqVMnDJdpoQgy27FS"
    "PImDyOEnvxyTnC9IRHmofzPsn49UFAzcpXLHwTmRKHm6LyhD2CPv0EqzPpaEAxIN5HFrJt"
    "voVC6ZYy09XC1dCaettZ9Ct372bfrou+Hk+wz3Ioeegi5DaiQO2Pn0C0JBHULvHsBt3ulO"
    "DJ/LVoGXqJJl6QJOiL9Kcl1NkmGM+yL5wzaG6ABoLMEKIabjy9HNtH/5IXeEPu9PR6qlq6"
    "2rgrXzqqBZCmJ9Hk/fWuqr9XVyNSqetNN+068FYcMANids3ayd83nUtQ1dg3DmY1fvqR01"
    "lj0u2/tctyJyk6IaI3nCqmLuqI4IbpEzsTy8nuU87Haoo9RHgDxWtJmE2VDHBpPJ+5wWg/"
    "G0UM8+Xg5G151TLYLshKN9d3JeyEidY7+J7UGWFjI2E+jWd1dN31T0NtxU9Eq7AzVpGHUR"
    "5y3PTNPJ/2dycvxPa/tXE38nRp/SHUDxiF88NjXIW87Bf5y4vb6/DCUpHmUru87NWtr5xL"
    "hacw3j8W5t/68wnzBE1DJVaPblpXRcb0yNPR3WD/FOfc/DQVmnHR8LJA4ReB7v6flzfDVI"
    "Es04N9THPiJUoD4k85UDKuVBB5f6HNPi/tNiopiVl8O6owzyUpY0rtZKC3Rfy6rWe4Qxy/"
    "b4ImEW/nbeJJ7BpfDBfw+Vnxqt/CYq7+LZbbS3Z43m9uDrfwEyXu5W"
)
