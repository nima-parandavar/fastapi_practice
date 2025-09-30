from datetime import timedelta, datetime, timezone
from config import config as app_config
from models import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from services import Hasher
from services import JWT


class AuthRepository:
    def __init__(self):
        self.model = UserModel

    async def authentication_user(
        self,
        db: AsyncSession,
        username: str,
        password: str,
    ):
        hasher = Hasher()

        stat = select(self.model).filter(self.model.email == username)
        result = await db.execute(stat)
        user = result.scalars().first()

        if not user:
            return False

        if not hasher.check_password(password, user.password):
            return False

        return user

    def generate_jwt_token(
        self,
        data: dict,
        expires_delta: timedelta | None = None,
    ):
        jwt = JWT()
        to_encoded = data.copy()
        expire = datetime.now() + (
            expires_delta or timedelta(minutes=app_config.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        to_encoded.update({"expire": expire.timestamp()})
        return jwt.encode(to_encoded)
