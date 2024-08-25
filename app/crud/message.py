from datetime import datetime

from fastapi import Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Message, User
from app.core.db import AsyncSessionLocal
from app.core.db import get_async_session


class CRUDMessage(CRUDBase):

    async def get_last_messages(
            self,
            meeting_room_id: int,
            session: AsyncSession,
    ):
        """
        Последние 7 сообщений для чата переговорной.
        """
        db_objs = await session.execute(
            select(self.model).where(
                self.model.meeting_room_id == meeting_room_id).order_by(
                self.model.write_time.desc()).limit(7)
        )
        db_objs = db_objs.scalars().all()
        return db_objs


    async def add_message_data_to_database(
            self,
            text: str,
            user: User,
            meeting_room_id: int,
            time_of_msg: datetime,
    ):
        async with AsyncSessionLocal() as session:
            stmt = insert(self.model).values(
                message=text,
                user_id=user.id,
                meeting_room_id=meeting_room_id,
                write_time=time_of_msg,
            )
            await session.execute(stmt)
            await session.commit()




message_crud = CRUDMessage(Message)
