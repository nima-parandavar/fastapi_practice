from fastapi import APIRouter
from services import AuthFormData, db_session, TokenType
from repositories import AuthRepository
from schemas.auth import Token
from schemas.user import ResponseUser

router = APIRouter()


@router.post("/token", response_model=Token)
async def login(form_data: AuthFormData, db_session: db_session):
    """
    Login user with email and password
    """
    auth = AuthRepository()
    return await auth.login(db_session, form_data.username, form_data.password)


@router.get("/me", response_model=ResponseUser)
async def get_user_me(token: TokenType, db_session: db_session):
    """
    Get authenticated user info
    """
    auth = AuthRepository()
    return await auth.get_current_user_info(token, db_session)
