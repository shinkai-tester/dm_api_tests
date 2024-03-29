from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Any, List, Optional
from pydantic import BaseModel, Field, StrictStr, ConfigDict
from apis.dm_api_account.models.rating import Rating
from apis.dm_api_account.models.roles import UserRole


class BbParseMode(Enum):
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


class InfoBbText(BaseModel):
    model_config = ConfigDict(extra='forbid')

    value: Optional[StrictStr] = Field(None, description='Text')
    parse_mode: Optional[BbParseMode] = Field(None, alias='parseMode')


class PagingSettings(BaseModel):
    model_config = ConfigDict(extra='forbid')

    posts_per_page: Optional[int] = Field(
        None, alias='postsPerPage', description='Number of posts on a game room page'
    )
    comments_per_page: Optional[int] = Field(
        None,
        alias='commentsPerPage',
        description='Number of commentaries on a game or a topic page',
    )
    topics_per_page: Optional[int] = Field(
        None,
        alias='topicsPerPage',
        description='Number of detached topics on a forum page',
    )
    messages_per_page: Optional[int] = Field(
        None,
        alias='messagesPerPage',
        description='Number of private messages and conversations on dialogue page',
    )
    entities_per_page: Optional[int] = Field(
        None, alias='entitiesPerPage', description='Number of other entities on page'
    )


class UserSettings(BaseModel):
    model_config = ConfigDict(extra='forbid')

    color_schema: Optional[ColorSchema] = Field(None, alias='colorSchema')
    nanny_greetings_message: Optional[StrictStr] = Field(
        None,
        alias='nannyGreetingsMessage',
        description="Message that user's newbies will receive once they are connected",
    )
    paging: Optional[PagingSettings] = None


class UserDetails(BaseModel):
    model_config = ConfigDict(extra='forbid')

    login: Optional[StrictStr] = Field(None, description='Login')
    roles: Optional[List[UserRole]] = Field(None, description='Roles')
    medium_picture_url: Optional[StrictStr] = Field(
        None, alias='mediumPictureUrl', description='Profile picture URL M-size'
    )
    small_picture_url: Optional[StrictStr] = Field(
        None, alias='smallPictureUrl', description='Profile picture URL S-size'
    )
    status: Optional[StrictStr] = Field(None, description='User defined status')
    rating: Optional[Rating] = None
    online: Optional[datetime] = Field(None, description='Last seen online moment')
    name: Optional[StrictStr] = Field(None, description='User real name')
    location: Optional[StrictStr] = Field(None, description='User real location')
    registration: Optional[datetime] = Field(
        None, description='User registration moment'
    )
    icq: Optional[StrictStr] = Field(None, description='User ICQ number')
    skype: Optional[StrictStr] = Field(None, description='User Skype login')
    original_picture_url: Optional[StrictStr] = Field(
        None, alias='originalPictureUrl', description='URL of profile picture original'
    )
    info: Optional[Any] = None
    settings: Optional[UserSettings] = None


class UserDetailsEnvelope(BaseModel):
    model_config = ConfigDict(extra='forbid')

    resource: Optional[UserDetails] = None
    metadata: Optional[Any] = Field(None, description='Additional metadata')
