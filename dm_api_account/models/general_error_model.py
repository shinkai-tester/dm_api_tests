from pydantic import StrictStr, BaseModel


class GeneralErrorModel(BaseModel):
    message: StrictStr
