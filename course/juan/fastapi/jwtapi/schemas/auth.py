from pydantic import BaseModel


class LoginInRequest(BaseModel):
    email: str
    password: str

class TokenDto(BaseModel):
    access_token: str
    token_type: str = 'bearer'