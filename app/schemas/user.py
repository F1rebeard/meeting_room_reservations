from typing import Optional

from fastapi_users import schemas
from pydantic import Field, field_validator

class UserBase(schemas.BaseUser[int]):
    username: str = Field(
        ...,
        max_length=20,
        min_length=5,
        title='Псевдоним'
    )
    first_name: str = Field(
        ...,
        min_length=3,
        max_length=20,
    )
    last_name: str = Field(
        ...,
        min_length=2,
        max_length=30,
    )
    phone_number: Optional[str] = Field(
        None,
        min_length=4,
        max_length=4
    )


class UserRead(UserBase):
    pass


class UserCreate(schemas.BaseUserCreate):
    username: str = Field(
        ...,
        max_length=20,
        min_length=5,
        title='Псевдоним'
    )
    first_name: str = Field(
        ...,
        min_length=3,
        max_length=20,
    )
    last_name: str = Field(
        ...,
        min_length=2,
        max_length=30,
    )
    phone_number: Optional[str] = Field(
        None,
        min_length=4,
        max_length=4
    )

    @field_validator('phone_number')
    def check_phone_number_is_digit(cls, value: str) -> str:
        if not value.isdigit():
            raise ValueError('Номер телефона должен состоять из цифр!')
        return value


class UserUpdate(UserBase, schemas.BaseUserUpdate):
    pass
