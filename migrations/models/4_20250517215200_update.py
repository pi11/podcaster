from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "podcast" ADD "thumbnail_url" VARCHAR(512);
        ALTER TABLE "podcast" ALTER COLUMN "filesize" SET DEFAULT 0;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "podcast" DROP COLUMN "thumbnail_url";
        ALTER TABLE "podcast" ALTER COLUMN "filesize" DROP DEFAULT;"""


MODELS_STATE = (
    "eJztWm1z2jgQ/isef6IzuU7whbZz34CQKdcmdBLa67ST8QhLGE1tybXkplyH/36SX2U7Bs"
    "exIc3xibBSdlfPs9qVVvzSXQqRw14OkY+tlf6X9ksHnic+4wH9RNMJcFEmSaaKAQ4WTjgC"
    "UhEmEP1ETAi/3oqvLiDARlB8JYHjCAFYMO4DiwvJEjgMCZH3zVxi5MDQeGILQ6ktIPh7IL"
    "9zP5BTIVqCwOGZusgczGZIeexVoh8uTIs6gUsyvZBawg1M7EyTjQjyAVd1hV6ZfO2FHk0J"
    "vwjdFCMWJXIZmHAWem3LGX8Y/bPXZ2/+fHX2RkwJXUglrzeh98zysccxJZldb81XlKRWhE"
    "o98jmzHtkIfbia65vN/QtYxjBm2BtuQUINWpBAwIEiyvD/gXwm/VRJSAGtZiGZsosGRf0O"
    "LpJ/z5MxXgG/kg0X/DQdRGwu49kYDOpiL5Rswf7T8Hr8dnjdEwpfyGlUhHEU/VfxkBGNSY"
    "IyIOVu6gjEWHXHAPZPT9sFUCisBDAcywMonOMo2hVdgKiobwTk3zezqyog6+L2kYjRrxBb"
    "/ERzMOO3W1CU9uSwy9h3RwWvdzn8XMR1/H42kiKPMm77oZZQwUhgfFvlXISyyamN+Ar5Sa"
    "pYAOvbHfChWUo06Ughv8jlxzXjhga+hWqVl3iqWl5YKjqWl72XFz0ihGm9NQ14sECatQKE"
    "CKrCaGu37AS+0w0xseKOc+Wg7Vw52JIrB+VcGX52lCgT3V3X67YhNLZAaJQhdDExYSBWs/"
    "v0c9oIx6KBRng+nWxRLiM7EsaDykvGS1YD2gruJriPYi8v3l0jJ6WwYdmPC94HCi3AEqQz"
    "XXFy29QssYmaOjVWMZkWWS+THavsk7jEHT74xZpEvCAe5fDhzXh4PpFe+OAupTt2zoxIyc"
    "N9QX2EbfIOrUPUpwJwQKKFPG7PZIfEyi1zPIcc7hyy5mZXez9V3XnfoO22wZauwTM8xx06"
    "BC0fyZWYoHHnAAScmoTePQDbvNFGCJ+LUY5dVImyMAFnxFknua4myDDW+zL5Q1eWaAKobM"
    "EKIubTy8nNfHj5Idd+OB/OJ3LECKXrgrT3qsBZqkT7Zzp/q8mv2pfZ1aTYpUjnzb8UiA08"
    "2B6xdbN2zuaR1y549YKFg63wTG3Ktexx295nuhOS2yRVWckTZhUzU05EcAedieTh9Sxnod"
    "mljlIHAfJY0hZCzZY6NprN3ue4GE3nhXr28XI0ue71QxLEJBydu5P7QgbqEjttHA+ytJCh"
    "maju/HTVdpdnsKXLMyidDmTQ+NRCjHUcmaqR/09wMvzvrgBt1jxTlf/mjTMVM74K3AUB2D"
    "GLF8/2dnbJRtcXgL7R8gWgb1RfAORYHtNcW6KLi1TOwG8ejHt9DBwLUGzqr/U6rcp08onS"
    "q7QU4bFZuf8nwU8YIqqpLLT7DFjqf7TGxp66H4f40cQ9LzFlnhq+vgg9hONlfEliz/EZJk"
    "k009xSH/sqU6H1IZmv7FApD5q4NOeYFvefFhPGtDwd2h31IStlSaVXWdqg+9pWtR54lCjb"
    "4xOPWvi7eeR5Bl32g/84Lx8anfxAL2/i2R20d2eN9s7gm/8AggS9/g=="
)
