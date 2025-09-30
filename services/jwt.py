from config import config as app_config
from exceptions import AuthException
import jwt


class JWT:
    def __init__(self, algorithm: str | None = None):
        self._secret_key = app_config.SECRET_KEY
        self._algorithm = algorithm if algorithm else app_config.ALGORITHM

    def encode(self, payload: dict):
        return jwt.encode(
            payload,
            key=self._secret_key,
            algorithm=self._algorithm,
        )

    def decode(self, token: str):
        try:
            payload = jwt.decode(
                token, key=self._secret_key, algorithms=[self._algorithm]
            )
            return payload
        except jwt.exceptions.InvalidTokenError:
            raise AuthException.credentials
