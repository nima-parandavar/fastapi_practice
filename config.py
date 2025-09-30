import os
from passlib.context import CryptContext
from zoneinfo import ZoneInfo


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
    SECRET_KEY = "3b333fc4fd46c836a2963abff26ec8ba95b69e07450a8984e28194a0ffc26167"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    TIME_ZONE = ZoneInfo("Asia/Tehran")


config = Config
