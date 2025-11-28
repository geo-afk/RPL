import structlog
from typing import Dict, Any
from fastapi import APIRouter
from pydantic import BaseModel
from starlette import status
from starlette.websockets import WebSocket, WebSocketDisconnect
from app.api.services.connection_manager import ConnectionManager
from app.api.services.rpl_editor_service import analyze_policies

logger = structlog.get_logger(__name__)
rpl_router = APIRouter(
    prefix="/code",
    tags=["rpl_code"],
)

manager = ConnectionManager()


class PolicyResponse(BaseModel):
    message: Dict[str, Any]

class PolicyRequest(BaseModel):
    code: str
    use_llm: bool = False



# policies: str,use_llm: bool,
@rpl_router.post(
    "/analyze",
    status_code=status.HTTP_201_CREATED,
    response_model=PolicyResponse,
    summary="Create or analyze policies send by client",
    description="Saved the models of the policies to client_db of analyze them with AI"
)
async def analyze_code(request: PolicyRequest):
    result: Dict[str, Any] | None = await analyze_policies(
        code=request.code,
        use_llm=request.use_llm
    )

    if result:
        logger.info(f"Result: {result}")
        return PolicyResponse(message=result)

    return PolicyResponse(message={"unseen": "unseen events"})



# @router.websocket(
#     "/ws/editor/{client_id}",
#     name="Get the rpl code and run checks to see if good",
# )
# async def websocket_endpoint(websocket: WebSocket, client_id: int):
#     await manager.connect(websocket)
#
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await manager.send_personal_message(f"Message text was: {data}", websocket)
#     except WebSocketDisconnect:
#         await manager.broadcast(f"Client #{client_id} disconnected")
