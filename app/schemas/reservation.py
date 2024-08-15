from datetime import datetime, timedelta

from pydantic import (BaseModel, ConfigDict, Field,
                      field_validator, model_validator)
from typing_extensions import Optional

FROM_TIME = (
        datetime.now() + timedelta(minutes=10)
).isoformat(timespec='minutes')

TO_TIME = (
        datetime.now() + timedelta(hours=1)
).isoformat(timespec='minutes')


class ReservationBase(BaseModel):
    from_reserve: datetime = Field(..., examples=[FROM_TIME])
    to_reserve: datetime = Field(..., examples=[TO_TIME])

    model_config = ConfigDict(extra='forbid')


class ReservationUpdate(ReservationBase):
    pass

    @field_validator('from_reserve')
    def check_from_reserve_later_than_now(cls, value: datetime) -> datetime:
        if value <= datetime.now():
            raise ValueError('Время бронирование меньше текущего времени!')
        return value

    @model_validator(mode='before')
    def check_from_reserve_before_to_reserve(cls, values):
        if values['from_reserve'] >= values['to_reserve']:
            raise ValueError(
                'Время начала бронирования '
                'не может быть больше времени окончания'
            )
        return values


class ReservationCreate(ReservationUpdate):
    meetingroom_id: int


class ReservationDB(ReservationBase):
    id: int
    meetingroom_id: int
    user_id: Optional[int]

    model_config = ConfigDict(from_attributes=True)
