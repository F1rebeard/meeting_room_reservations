from datetime import datetime
from typing import Optional

from fastapi.params import Depends
from sqlalchemy import select, and_, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.user import current_user
from app.crud.base import CRUDBase
from app.models import Reservation, User

class CRUDReservation(CRUDBase):

    async def get_reservations_at_the_same_time(
            self,
            *,
            from_reserve: datetime,
            to_reserve: datetime,
            meetingroom_id: int,
            reservation_id: Optional[int] = None,
            session: AsyncSession,
    ) -> Sequence[Reservation]:
        select_stmt = select(Reservation).where(
                Reservation.meetingroom_id == meetingroom_id,
                and_(
                    from_reserve <= Reservation.to_reserve,
                    to_reserve >= Reservation.from_reserve
                )
            )
        if reservation_id:
            select_stmt = select_stmt.where(
                Reservation.id != reservation_id
            )
        reservations = await session.execute(select_stmt)
        reservations = reservations.scalars().all()
        return reservations

    async def get_future_reservations_for_room(
            self,
            room_id: int,
            session: AsyncSession,
    ):
        reservations = await session.execute(
            select(Reservation).where(
                Reservation.meetingroom_id == room_id,
                Reservation.to_reserve > datetime.now()
            )
        )
        reservations = reservations.scalars().all()
        return reservations

    async def get_current_user_reservations(
            self,
            session: AsyncSession,
            user: User,
    ) -> Sequence[Reservation]:
        user_reservations = await session.execute(
            select(Reservation).where(
                Reservation.user_id == user.id
            )
        )
        user_reservations = user_reservations.scalars().all()
        return user_reservations


reservation_crud = CRUDReservation(Reservation)
