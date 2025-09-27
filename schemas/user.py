from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    email: EmailStr
    full_name: str | None


class ResponseUser(BaseUser):
    id: int

    class Config:
        from_attributes = True


class CreateUser(BaseUser):
    password: str


class UpdateUser(BaseModel):
    full_name: str | None
