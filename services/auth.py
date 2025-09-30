from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token",
    description="Authentication for practice",
    refreshUrl="refresh",
)


AuthType = Annotated[str, Depends(oauth2_scheme)]
AuthFormData = Annotated[OAuth2PasswordRequestForm, Depends()]
TokenType = Annotated[str, Depends(oauth2_scheme)]
