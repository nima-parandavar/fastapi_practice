from fastapi import APIRouter
from services import AuthFormData
from services import db_session
from repositories import AuthRepository
from exceptions import AuthException
from schemas.auth import LoginResponse

router = APIRouter()


@router.post("/token", response_model=LoginResponse)
async def login(form_data: AuthFormData, db_session: db_session):
    print(form_data)
    auth = AuthRepository()
    user = await auth.authentication_user(
        db_session, form_data.username, form_data.password
    )
    if not user:
        raise AuthException.unauthorized
    token = auth.generate_jwt_token({"id": user.id})
    return {"token": token, "type": "bearer"}
