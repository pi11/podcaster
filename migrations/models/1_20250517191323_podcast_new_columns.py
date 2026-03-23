from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "podcast" ADD "filesize" INT NOT NULL;
        ALTER TABLE "podcast" ADD "file" VARCHAR(250);
        ALTER TABLE "podcast" ADD "is_processed" BOOL NOT NULL DEFAULT False;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "podcast" DROP COLUMN "filesize";
        ALTER TABLE "podcast" DROP COLUMN "file";
        ALTER TABLE "podcast" DROP COLUMN "is_processed";"""


MODELS_STATE = (
    "eJztWm1z2jgQ/isef+Jm0k7DhbZz34CQKW0TMgnt3bST8QhLgKZGciW5Kdfhv5/kN8l2DI"
    "5jkzTHJ/Bq2V09z2pXkvllryhEHn/ZRwy7S/sv65cNfF9+xgP2kWUTsEJakqjKAQFmXjgC"
    "UhEmEP1EXAq/3sjHFSBggaB8JIHnSQGYccGAK6RkDjyOpMj/5swx8mDoPPGFobIWEPw9UM"
    "+CBUoVojkIPKHNRe6g1lDyOKrEPpw5LvWCFdF2IXVlGJgstKUFIogBYdoKo3LE2g8jGhNx"
    "FoYpR1xK1DQwETyMeqE0XnSPT96cvP3z9clbqRKGkErebMLoucuwLzAl2q+/FktKUi/SpB"
    "3FrL1HPsIYLqb2ZnP3BOYxjBr77ionoV2ak0AggCHS+P9AjKs4TRJSQMtZSFR20WCY38FF"
    "8vMsGcMlYKVsrMBPx0NkIVQ+d3u9qthLI1uw/9y/Gr7rX3WkwT+UGpVpHGX/RTzUjcYUQR"
    "pItZpaAjE23TKAx69eNQugNFgKYDiWBVAGJ1C0KtoA0TBfC8j315OLMiCr4vaJyNGvELvi"
    "yPIwFzdbUFT+1PCK8++eCV7nvP9PHtfhx8lAiXzKxYKFVkIDA4nxTVlwEcqOoAskloglpW"
    "IG3G+3gEGnUGjSkVx9UdOPe8Y1DZiLKrWXWNVsLzwVHdrL3tuLHRHCrc6aBiKYIctdAkIk"
    "VWG2Ndt2Aua1Q0xsuOVa2Wu6Vva21MpesVaGny0VysR22/26aQi7WyDsRhAWS+GOpL9Xid"
    "T06DrWFEF1uBjEUZ59uEIeEPE2rGbriov2JYUu4Elt0bbiBbqp2CYSM1X6hOEybRS+lh06"
    "xZM4iDx+8ss5yXxBIqpD/eth/3SkomDgNqU7Ds6JSMnCfUYZwgvyAa1D1McScECiiTxsze"
    "iNTumSOfTSQy/9jSF0GVIzcUDt0xsIBHUIvb0HtlmntRA+laMCr1ApytIFnBBvnazViiDD"
    "2O7L5IttTNEB0FiDJURMx+ej62n//DJzBDztT0dqpBtK1zlp53WOs9SI9fd4+s5Sj9aXyc"
    "Uof1JM9aZfcsQGPmyO2KpVJ+PzwGsbvPrBzMNuuCd01Fz2uGzvct0KyU2SaszkCbOKuaMU"
    "EdxBZyK5fz/LeKh3KKHUQ4A8lLSZNLOljw0mk48ZLgbjaa6ffTofjK46xyEJUglH+8Zkv6"
    "tBnWOvie2BLgsazcR06zfjTZ+0e1tO2r3C7kAlDaPykM1bzkzTyf8nOTn+t7X9q2m/FqJP"
    "6QybP6I6eFc61sYt4+A3B26v7w+GEpQFZWu7ys1QqnxkXA25hvBwN7T/twifMUTUMllo9s"
    "1B4bjeGBt7Oqw/xnvWOy6+izzVvOyWdojA83hPz5/jrXdSaMaZqT70ErzE6n0qXzGgQh10"
    "cEHnUBb3XxYTxqwsHdYtZZAXqqRxtVZYoPtaVpXu040s2+ONutn427lTfwaXwo/+f55sar"
    "Tyn56si2e30d5dNZrbg2/+A1eTiJs="
)
