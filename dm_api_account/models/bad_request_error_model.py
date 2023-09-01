from typing import List, Dict
from pydantic import StrictStr, BaseModel


class BadRequestErrorModel(BaseModel):
    type: StrictStr
    title: StrictStr
    status: int
    traceId: StrictStr
    errors: Dict[str, List[str]]
