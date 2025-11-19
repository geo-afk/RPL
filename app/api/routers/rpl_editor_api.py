import structlog
from fastapi import APIRouter
from starlette.websockets import WebSocket, WebSocketDisconnect
from app.api.services.connection_manager import ConnectionManager


logger = structlog.get_logger(__name__)
router = APIRouter()

manager = ConnectionManager()


@router.websocket(
    "/ws/editor/{client_id}",
    name="Get the rpl code and run checks to see if good",
)
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"Message text was: {data}", websocket)
    except WebSocketDisconnect:
        await manager.broadcast(f"Client #{client_id} disconnected")
