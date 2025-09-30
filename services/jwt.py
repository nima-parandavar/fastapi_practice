from datetime import datetime
from config import config as app_config
from exceptions import AuthException
import jwt
from schemas.auth import Payload


class JWT:
    def __init__(self, algorithm: str | None = None):
        self._secret_key = app_config.SECRET_KEY
        self._algorithm = algorithm if algorithm else app_config.ALGORITHM

    def encode(self, payload: dict) -> str:
        return jwt.encode(
            payload,
            key=self._secret_key,
            algorithm=self._algorithm,
        )

    def decode(self, token: str) -> Payload:
        try:
            payload = jwt.decode(
                token, key=self._secret_key, algorithms=[self._algorithm]
            )
            return Payload(**payload)
        except jwt.exceptions.InvalidTokenError:
            raise AuthException.credentials

    def verify(self, token: str) -> Payload:
        decode_token = self.decode(token)
        if datetime.now().timestamp() > decode_token.expire:
            raise AuthException.token_expire
        return decode_token
