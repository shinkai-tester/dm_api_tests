from pydantic import BaseModel, StrictStr, Field


class LoginCredentialsModel(BaseModel):
    login: StrictStr
    password: StrictStr
    remember_me: bool = Field(alias='rememberMe')
