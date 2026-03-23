from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "podcast" ADD "bitrate" VARCHAR(10);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "podcast" DROP COLUMN "bitrate";"""


MODELS_STATE = (
    "eJztW21z2jgQ/isMn9KZXichoe3cNyCk5ZqETkJ7nXYyHmELo4mRXFsO8XXy30+S32Qbgz"
    "EWIYQvTSMpu6tnV1rti/80Z8SAlvuuAx2kT5t/N/40gW2zn+FE822jicEMJiPRUjZBwdgS"
    "MyAeQtiAj9Blg7/u2K8zgIEJDfYr9iyLDYCxSx2gUzYyAZYL2ZB9r00QtAzBPOKFDE7Nw+"
    "i3x3+njseXGnACPIsm5AJ2RrKCj4dSRfSNsaYTy5vhhK5BdCYGwmZCyYQYOoDKtIRUGvVt"
    "IdEA0wshJpvRCebbQJi6QmqTr/irdXL24ezj6fuzj2yJECEe+fAkpHd1B9kUEZzwtX06JT"
    "jmwkg2A5kT7gEPIcP1qPn0tHgDkxDGBPvWLDNCWiQzYgAKpKEE/wfouFxOWQkxoMVaiJas"
    "UoNEfoUuoj9PK6M3BU6hNmbgUbMgNim351a7XRZ7RmQJ9t87N73PnZsjRvANX0aYGQfWfx"
    "1OtYI5rqAESH6aFIEYklYM4Mnxcb0AMoKFAIq5NIBMOAqDU6ECRIl8JSD/uR1eFwFZFrdv"
    "mM3+MpBO3zYs5NK7JShyfnx65rq/LRm8o6vOjyyuvcthlw/ZxKWmI6gIAl2G8V2RcAHKGi"
    "UmpFPoRFfFGOj3c+AYWu6iiWcy9wvffugzbonn6LCUewmXyu7FjYcO7mXr7qUZKMRtHPnE"
    "o94YNvQpwJipSlhbyhoSgKmphctqOLiResqdT7ZdZkiQBvdc57bXOe9zIRwwjy1Bkk8LdJ"
    "bWxgVxIDLxF+gLpQyYPgAOTLDiGQ+te2T2EliE6UTUwn0+bey6PcdSY9whYcX+pl23v2kv"
    "8TftvL8RPxU5m4i26jdP3RC2lkDYykM4Q+wIemw3q1+Qx5VwzDKohOcu3bgJdgRbvuZAS4"
    "i+HLtoZH38skwq4dclxIIAb/r4GTMySxDqDoeXqfdOdzDKmOK3q26fPSuFhbJFKLj589Dy"
    "M/KADEhczYZOSf900q5moYW89shWc060Jj8vA5nj8cLxyz+7Vzyw1nqOJ7pJ3sx1ObJKd0"
    "Qo5cWXG37bhNf1Zk+or8TQgRshvfgBVSIkiciUiUkklnFQYidjh6hkJ5Jez2/8pUKPQLjt"
    "hh1JUF0y5pDyL2yPJnEQdKsZJ506xDOn0pHRQpJ+UwnY2upr6Qpgf0T4vzmcBWBa5vz3JI"
    "HLKmJCHHED3UNfgtEP9b5YTTKf+AoLCUTgBX8fPt60xVoqVPIhjNxWGOnT7JuoNgBj0spT"
    "53VnzpckzvcwDH9uE5QZq3mcZzhUwnMEHwvfGPXAN+r/GC1Pmc/8cOZyeP0pWp7No2fKEg"
    "4UFzCoXJkAHiUaJvM1DDfNtBLc52yWohksNGHGwhhiy4/cRkkVGCHdd9F/mtIWNWAYKRNa"
    "qKbBVf921Ln6mtLVeWfU5zOtlJ6i0aP3mQMRE2n8Oxh9bvBfGz+H1/1sFSReN/qZUaxnG/"
    "UptqxLTPE86FWFXm1vbCFdxKAa38sWj+0i1kqUXKdSpZ3ssFaRq7HAGj2sUmdoouu/FVIM"
    "XkeelG2Zg68w/5zi8GpABXOAKNun2LtKbHOMXg3EtkN06LqKTVdm8mqgNcgcWwQYarFNc3"
    "kd4E6QVUeouyhAi0grzxTUXXBuLyk4t3ORLt+mi/5bhWK1YrNM/IUXn1LFu6k3G2OALC2b"
    "6auxeJfloTrjctKqOeNy0irOuPC5AkxV47mNM/3MTSRjRJ0NwrQVSErUlffP1t0+u6R7Ng"
    "tiqtakIpWaYvDCb8etdsTGpZ4y9We5LhQXoOUq2qECvf2+2O+8vacha2HFJxj7UlNdqKd1"
    "S6pSS0XFimq6ILqyVyRbT80UZNUXVHMVrdpO15bqWc/xJciCdqn8uavYIsXoYIomYWbWrd"
    "NF7kqvVOQ4BqmtLrXoEr4raWIv47xSLe+x96Km1BN5cF870UC18acHe1C0f+7P3aiprG8k"
    "Jq0YwtOaETwtBvA0h5+oYilNsKc47G+Gsp5oaCe+CFPvZ0v0V64RE2a89ToRYt7R5+JFDe"
    "XWHPzv9sPHSGONtDoac+IYbi6azMWOfp1+tsbu5kxYtaX+ZjlBouarysPTZvMv+dOmoeRr"
    "/jSLvUtIrr416stVPv0PrOiSsg=="
)
