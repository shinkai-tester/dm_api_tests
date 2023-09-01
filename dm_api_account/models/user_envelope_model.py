from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, StrictStr, Field

from dm_api_account.models.rating import Rating
from dm_api_account.models.roles import Roles


class User(BaseModel):
    login: StrictStr
    roles: List[Roles]
    medium_picture_url: Optional[StrictStr] = Field(None, alias="mediumPictureUrl")
    small_picture_url: Optional[StrictStr] = Field(None, alias="smallPictureUrl")
    status: Optional[StrictStr] = Field(None)
    rating: Rating
    online: Optional[datetime] = Field(None)
    name: Optional[StrictStr] = Field(None)
    location: Optional[StrictStr] = Field(None)
    registration: Optional[datetime] = Field(None)


class UserEnvelopeModel(BaseModel):
    resource: User
    metadata: Optional[StrictStr] = Field(None)
