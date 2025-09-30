from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class Payload(BaseModel):
    sub: str
    expire: float

    def get_user_id(self):
        return int(self.sub.split(":")[-1])
