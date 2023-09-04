from typing import Optional
from pydantic import BaseModel, StrictStr, Field, Extra


class LoginCredentials(BaseModel):
    class Config:
        extra = Extra.forbid

    login: Optional[StrictStr] = None
    password: Optional[StrictStr] = None
    remember_me: Optional[bool] = Field(None, alias='rememberMe')
