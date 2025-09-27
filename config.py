import os
from passlib.context import CryptContext


class Config:
    DEBUG: bool = True if os.getenv("DEBUG") == "true" else False
    DB_CONFIG = os.getenv(
        "DB_CONFIG",
        "postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}".format(
            DB_USER=os.getenv("DB_USER"),
            DB_PASSWORD=os.getenv("DB_PASSWORD"),
            DB_HOST=os.getenv("DB_HOST"),
            DB_PORT=os.getenv("DB_PORT", 5432),
            DB_NAME=os.getenv("DB_NAME"),
        ),
    )
    PWD_CONTEXT = CryptContext(
        schemes=["pbkdf2_sha256", "des_crypt"], deprecated="auto"
    )


config = Config
