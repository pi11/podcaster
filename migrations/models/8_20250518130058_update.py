from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "podcast" ADD "thumbnail" VARCHAR(200);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "podcast" DROP COLUMN "thumbnail";"""


MODELS_STATE = (
    "eJztWm1z2jgQ/isef+Jmcp3gC23nvgEhV65J6CS012kn4xGWAE1tybXkEtrhv5/kV9nGQB"
    "wb0oRPxCtld/U8q11r5V+6QyGy2asu8rA11//WfunAdcVvNKCfaDoBDkol8VQxwMHEDkZA"
    "IsIEonvEhPDrnXh0AAEzBMUj8W1bCMCEcQ9YXEimwGZIiNxv5hQjGwbGY1sYSm0+wd99+c"
    "w9X06FaAp8m6fqQnMwnSHlkVexfjgxLWr7Dkn1QmoJNzCZpZpmiCAPcFVX4JXJl27g0ZDw"
    "i8BNMWJRIpeBCWeB1zM540+jffbm7O1fr8/eiimBC4nkzSrwnlkedjmmJLXrLvmcksSKUK"
    "mHPqfWQxuBD9djfbVav4BpBGOKveHkJNSgOQkEHCiiFP8fyGPST5WEBNByFuIp22hQ1G/h"
    "Iv73LBn9OfBK2XDAvWkjMuMyno1OZ1fshZIN2H/q3vTfdW9aQuEfchoVYRxG/3U0ZIRjkq"
    "AUSLmbGgIxUt0wgO3T03oBFApLAQzGsgAK5zgKd0UTICrqKwH57+3ougzIXXH7SMToV4gt"
    "fqLZmPG7DShKe3LYYey7rYLXuup+zuPavxz1pMiljM+8QEugoCcwvitzLkTZ5HSG+Bx5ca"
    "qYAOvbAnjQLCSaZCSXX+Tyo5pxS33PQjuVl2iqWl5YIjqWl72XFz0khGmtJfW5P0GaNQeE"
    "CKqCaKu37Pie3QwxkeKGc2Wn7lzZ2ZArO8VcGfw2lChj3U3X67ohNDZAaBQhdDAxoS9Ws/"
    "3t57QSjnkDlfB8OtmiWEa2JIwHlZeUl7QG1BXcVXDvRV5evL9BdkJhxbIfFbwPFFqAxUin"
    "uqLkttqxxMZqdqmxismkyLqp7Fhln8Qh7vDBL9Yk4gXxMId3b/vd84H0wgOLhO7IOTMkJQ"
    "v3BfUQnpH3aBmgPhSAAxIu5HF7Jn1JLN0yx/eQw72HLLnZ1N5PVDfeN6i7bbCha/AM3+MO"
    "HYKq4ccjGYevCmTOQiU8x+i+tCDVA9948Hm8uV/gLKORy9H1P/H0fBMh15PxkFyWCSq3ZY"
    "DPqUno4gGBmzVaCe5zMcqxg0pDWJiAI2Iv40KyIwUw0vsq/kNXlmgCCDMhtJam4dXgdty9"
    "+pDh6rw7HsgRI8NTLG29zm2IRIn233D8TpOP2pfR9SDfAkrmjb/kiPVdWB+xu5bEjM0jr0"
    "3w6voTG1vBgcWUa9njtl1nuhGS6yRVWckTZhUzU5zC8I9tdEYh+vB3hYyBagdmSm0EyGM5"
    "mwg1G4pcbzS6zFDRG+ar2Mer3uCm1Q44EJNweKaJz2IZTCX4CG7BNJZUAjW18HJA9aiFGG"
    "sYV9XIi4EW0gWxKYDNYpu18jLAnWK7jnPYutNDrLrxY2zd7fTOhnZ6p3AMk8tk+Oc2FKu1"
    "0lXlv3kbXcWMz31nQgC2zXwbqr7wK9houh3QNmpuB7SN8naAHCvBtGk8X8AVWabh20SLKm"
    "PgN9/Ye/3Moi9AmVFvqe9yCZRMPlFugSxFeLwG2v/HFp8wRFRTWaj3A4tCZ7k2NvbUVz7E"
    "52hr7riLPFW81xZ6CMfTqEPCnuMFd5xohpmlPva+u0TrQzJf0aFCHjRxYc4xLe4/LcaMaV"
    "k6tAX1ICtkSeWiorBB97Wtdro6V6Jsj5fnauFv5vr8GdxfHvyz52xoNPLpc9bEs3vR3p41"
    "6nsHX/0PGvJz1Q=="
)
