from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class MeetingRoomBase(BaseModel):
    name: str = Field(
        None,
        max_length=100,
        min_length=1,
        title='Название переговорки',
    )
    description: Optional[str] = Field(None)


class MeetingRoomCreate(MeetingRoomBase):
    name: str = Field(
        ...,
        max_length=100,
        min_length=1,
        title='Название переговорки',
    )


class MeetingRoomUpdate(MeetingRoomBase):

    @field_validator('name')
    def name_cannot_be_null(cls, value: str):
        if value is None:
            raise ValueError('Имя переговорки не может быть пустым!')
        return value


class MeetingRoomDB(MeetingRoomBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
