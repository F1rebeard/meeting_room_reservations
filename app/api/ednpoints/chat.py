from datetime import datetime

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request, \
    WebSocketException
from fastapi.params import Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, get_user_manager, auth_backend
from app.crud.message import message_crud
from app.models import User


router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()

templates = Jinja2Templates(directory="app/templates")


async def get_user_from_cookies(
        websocket: WebSocket,
        user_manager = Depends(get_user_manager)
):
    cookie = websocket.cookies.get('auth_cookie')
    user = await auth_backend.get_strategy().read_token(cookie, user_manager)
    if not user or not user.is_active:
        raise WebSocketException(code=1003, reason='Invalid user')
    yield user


@router.get(
    '/{meeting_room_id}',
)
def get_chat_page(
        request: Request,
        meeting_room_id,
        user: User = Depends(current_user),
):
    """
    Чат для переговорной комнаты через Websocket c сохранением сообщений в бд.
    """
    return templates.TemplateResponse(
        'chat.html',
        {
            'request': request,
            'meeting_room_id': meeting_room_id,
            'user': user,
        }
    )


@router.get(
    "/{meeting_room_id}/last_messages",
)
async def get_last_messages(
        meeting_room_id: str,
        session: AsyncSession = Depends(get_async_session)
):
    messages = await message_crud.get_last_messages(int(meeting_room_id), session)
    return [message.as_dict() for message in messages]


@router.websocket(
    "/{meeting_room_id}/ws/{client_id}",
)
async def websocket_endpoint(
        websocket: WebSocket,
        meeting_room_id: str,
        user: User = Depends(get_user_from_cookies),
):
    if user is None:
        return
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await message_crud.add_message_data_to_database(
                text=data,
                user=user,
                meeting_room_id=int(meeting_room_id),
                time_of_msg=datetime.now(),
            )
            await manager.broadcast(
                f"{user.first_name} {user.last_name}"
                f" ({datetime.now().strftime('%H:%M')}): {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(
            f"{user.first_name} {user.last_name} вышел из чата")
