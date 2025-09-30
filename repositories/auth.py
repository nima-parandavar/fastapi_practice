from datetime import timedelta, datetime
from config import config as app_config
from models import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from services import Hasher
from services import JWT
from schemas.user import ResponseUser
from schemas.auth import Token
from exceptions import UserException, AuthException


class AuthRepository:
    def __init__(self):
        self.model = UserModel

    async def _authentication_user(
        self,
        db: AsyncSession,
        username: str,
        password: str,
    ) -> ResponseUser | bool:
        hasher = Hasher()

        stat = select(self.model).filter(self.model.email == username)
        result = await db.execute(stat)
        user = result.scalars().first()

        if not user:
            return False

        if not hasher.check_password(password, user.password):
            return False
        return ResponseUser(**user.__dict__)

    def generate_jwt_token(
        self,
        data: dict,
        expires_delta: timedelta | None = None,
    ) -> str:
        jwt = JWT()
        to_encoded = data.copy()
        expire = datetime.now() + (
            expires_delta or timedelta(minutes=app_config.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        to_encoded.update({"expire": expire.timestamp()})
        return jwt.encode(to_encoded)

    async def get_current_user_info(
        self, token: str, db_session: AsyncSession
    ) -> ResponseUser:
        jwt = JWT()
        payload = jwt.verify(token)
        user_id = payload.get_user_id()
        stat = select(self.model).filter(self.model.id == user_id)
        result = await db_session.execute(stat)
        user = result.scalars().first()
        if not user:
            raise UserException.not_found
        return ResponseUser(**user.__dict__)

    async def login(
        self,
        db_session: AsyncSession,
        username: str,
        password: str,
    ) -> Token:
        user = await self._authentication_user(db_session, username, password)
        if not user:
            raise AuthException.unauthorized
        token = self.generate_jwt_token({"sub": f"identify:{user.id}"})
        return Token(access_token=token, token_type="bearer")
