from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, TIMESTAMP, String, UniqueConstraint, Integer

from app.core.db import Base

PHONE_NUMBER_LEN: int = 4


class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(20), unique=True, nullable=False)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(30), nullable=False)
    phone_number = Column(String(4))
    registered_at = Column(TIMESTAMP, default=datetime.now())
    UniqueConstraint('username', name='unique_username')
