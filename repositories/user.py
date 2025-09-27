from .base import BaseRepository
from models import UserModel
from schemas.user import CreateUser, UpdateUser
from services import Hasher


class UserRepository(BaseRepository[UserModel, CreateUser, UpdateUser]):
    def __init__(self):
        super().__init__(UserModel)

    async def create(self, db, body):
        hasher = Hasher()
        body.password = hasher.create_password(body.password)
        return await super().create(db, body)
