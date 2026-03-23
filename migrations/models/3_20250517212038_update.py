from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "source" ADD "min_duration" INT NOT NULL DEFAULT 0;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "source" DROP COLUMN "min_duration";"""


MODELS_STATE = (
    "eJztWu9v2jwQ/leifGJSN7W8ZZveb0CpxraWqWV7p01VZGITrAU7i511bOJ/n51fdpIG0j"
    "SBri+fIGdzd34e++5y5re5pBC57EUf+dhemP8av03geeIzHjCPDJOAJVKSZKoY4GDmhiMg"
    "FWEC0U/EhPDrjXhcAgIcBMUjCVxXCMCMcR/YXEjmwGVIiLxv1hwjF4bGE1sYSm0Bwd8D+c"
    "z9QE6FaA4Clyt1kTmoZkh57FWiH84sm7rBkii9kNrCDUwcpclBBPmA67pCryy+8kKPxoSf"
    "h26KEZsSuQxMOAu9duSM592T01enr/95efpaTAldSCWv1qH3zPaxxzElyq634gtKUitCpR"
    "n5rKxHNkIfLqfmen33AuYxjAr77jInoV2ak0DAgSZS+P9APpN+6iSkgJazkEzZRoOmfgsX"
    "yc+zZAwXwC9lYwl+Wi4iDpf7udvrVcVeKNmA/af+1fBN/6ojFD6T06jYxtHuv4yHutGYJE"
    "gBKU9TSyDGqlsG8OT4uFkAhcJSAMOxLIDCOY6iU9EGiJr6WkC+vZ5clgFZFbePRIx+hdjm"
    "R4aLGb/ZgKK0J4eXjH13dfA6F/3PeVyH7ycDKfIo444fagkVDATGN2XORShbnDqIL5CfhI"
    "oZsL/dAh9ahUCTjuTii1x+nDOuaeDbqFJ6iafq6YWlokN62Xl6MSNCmNFZ0YAHM2TYC0CI"
    "oCrcbc2mncB32yEmVtxyrOw1HSt7G2Jlrxgrw8+WAmWiu+183TSE3Q0QdosQLjGxYCBWs7"
    "36Oa6FY95ALTwfT7QoppEtAeNe6UXxonJAU5u7Du6D2Mvzd1fITSmsmfbjhPeBQhuwBGml"
    "Kw5u64opNlFTJcdqJtMk6ynZIcs+ipe4/W9+sSaxXxCPYnj/etg/G0kvfHCb0h07Z0WkZO"
    "E+pz7CDnmHViHqYwE4INFCHnZmVJFYemQOdcj+6pAVt9o6+6nq1vsGTbcNNnQNnmAdt+8t"
    "aPtIrsQCtTsHIODUIvT2HthmjdZC+EyMcrxEpSgLE3BC3FUS6yqCDGO9L5IvprZEC0DtCJ"
    "YQMR1fjK6n/YsPmfbDWX86kiPdULrKSTsvc5ylSoz/xtM3hnw0vkwuR/kuRTpv+iVHbODB"
    "5oitGrUzNg+8tsGrF8xcbIc1tSXXssNje5fpVkhuklRtJY+YVcwsORHBLXQmkvvns4yFei"
    "91lLoIkIeSNhNqNuSxwWTyPsPFYDzN5bOPF4PRVeckJEFMwlHdnbwvKFDn2G2iPFBhQaGZ"
    "qG69umq6y9Pb0OXpFaoDuWl8aiPGWt6ZupH/z+Zk+Fdr9auu/y/vnemwZd6i28AtY+AvB2"
    "6nd1dDAYpD/ZVZpbOWTj7SWmu2Jjz01nZ/g/UJQ0QNnYVmb60Kr+uNsbGjl/V93PHfcXFQ"
    "5KnmZYHQQziexzU9e4q3BkmgGWeW+tBLhBKt94l8RYcKcdDChTmHsLj7sJgwZmTpMG6pD1"
    "khSmqttcIB3dWxqnQfoe2yHd5I6Im/nTuJJ9AU3vt/ybJbo5X/k2VNPLlCe3vUaK4GX/8B"
    "sLBSNg=="
)
