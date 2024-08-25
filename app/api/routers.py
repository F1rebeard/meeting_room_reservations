from fastapi import APIRouter, Request

from app.api.ednpoints import (meeting_room_router, reservation_router,
                               user_router, chat_router)
from app.api.ednpoints.chat import templates

api_main_router = APIRouter()
api_main_router.include_router(
    meeting_room_router, prefix="/meeting_rooms", tags=["Meeting Rooms"])
api_main_router.include_router(
    reservation_router, prefix="/reservations", tags=["Reservations"]
)
api_main_router.include_router(
    chat_router, prefix="/chat", tags=["Chat"]
)
api_main_router.include_router(user_router)

# @api_main_router.get("/long_operation")
# @cache(expire=30)
# async def get_long_operation():
#     await asyncio.sleep(3)
#     return 'Вычисление большого количества данных'