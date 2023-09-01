from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, StrictStr, Field

from dm_api_account.models.rating import Rating
from dm_api_account.models.roles import Roles


class ParseModes(Enum):
    COMMON = 'Common'
    INFO = 'Info'
    POST = 'Post'
    CHAT = 'Chat'


class ColorSchema(Enum):
    MODERN = 'Modern'
    PALE = 'Pale'
    CLASSIC = 'Classic'
    CLASSIC_PALE = 'ClassicPale'
    NIGHT = 'Night'


class InfoBpText(BaseModel):
    value: Optional[StrictStr] = Field(None)
    parse_mode: Optional[ParseModes] = Field(None, alias="parseMode")


class PagingSettings(BaseModel):
    posts_per_page: int = Field(alias="postsPerPage")
    comments_per_page: int = Field(alias="commentsPerPage")
    topics_per_page: int = Field(alias="topicsPerPage")
    messages_per_page: int = Field(alias="messagesPerPage")
    entities_per_page: int = Field(alias="entitiesPerPage")


class UserSettings(BaseModel):
    color_schema: ColorSchema
    nanny_greetings_message: StrictStr
    paging: PagingSettings


class UserDetails(BaseModel):
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
    icq: Optional[StrictStr] = Field(None)
    skype: Optional[StrictStr] = Field(None)
    original_picture_url: Optional[StrictStr] = Field(None, alias="originalPictureUrl")
    info: InfoBpText
    settings: UserSettings


class UserDetailsEnvelopeModel(BaseModel):
    resource: UserDetails
    metadata: StrictStr
