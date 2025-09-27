from config import config


class Hasher:
    """
    create and verify password
    """

    def __init__(self):
        self._pwd_context = config.PWD_CONTEXT

    def create_password(self, password: str):
        return self._pwd_context.hash(password)

    def check_password(self, raw_password: str, hashed_password: str):
        return self._pwd_context.verify(raw_password, hashed_password)
