from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.meeting_room import MeetingRoom


class CRUDMeetingRoom(CRUDBase):

    async def get_room_id_by_name(
            self,
            room_name: str,
            async_session: AsyncSession,
    ) -> Optional[int]:
        db_room_id = await async_session.execute(
            select(self.model.id).where(
                self.model.name == room_name
            )
        )
        db_room_id = db_room_id.scalars().first()
        return db_room_id


meeting_room_crud = CRUDMeetingRoom(MeetingRoom)
