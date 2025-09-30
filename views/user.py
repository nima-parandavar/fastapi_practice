from typing import Any
from fastapi import APIRouter
from fastapi import status
from schemas.user import CreateUser, ResponseUser
from services import db_session, AuthType
from repositories import UserRepository


router = APIRouter()


@router.post(
    "/create", status_code=status.HTTP_201_CREATED, response_model=ResponseUser
)
async def create(body: CreateUser, db: db_session) -> Any:
    userRepo = UserRepository()
    user = await userRepo.create(db, body)
    return user


@router.put("/{id}")
async def update(id: int, db: db_session, token: AuthType): ...
