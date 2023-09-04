from typing import Optional
from pydantic import StrictStr, BaseModel, Extra, Field


class GeneralError(BaseModel):
    class Config:
        extra = Extra.forbid

    message: Optional[StrictStr] = Field(None, description='Client message')
