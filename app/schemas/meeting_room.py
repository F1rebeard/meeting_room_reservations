from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class MeetingRoomBase(BaseModel):
    name: str = Field(
        None,
        max_length=100,
        min_length=1,
        title='Название переговорки',
    )
    description: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class MeetingRoomCreate(MeetingRoomBase):
    name: str = Field(
        ...,
        max_length=100,
        min_length=1,
        title='Название переговорки',
    )


class MeetingRoomDB(MeetingRoomBase):
    id: int
