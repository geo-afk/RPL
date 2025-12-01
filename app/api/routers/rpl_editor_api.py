import structlog
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette import status
from app.api.utils.connection_manager import ConnectionManager
from app.api.services.rpl_editor_service import analyze_policies, get_all_findings
from app.models.llm_result import Finding

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
        return PolicyResponse(message=result)

    return PolicyResponse(message={"unseen": "unseen events"})




@rpl_router.post(
    "/insight",
    status_code=status.HTTP_201_CREATED,
    response_model=List[Finding],
    summary="get all llm findings ",
    description="Get All LLM Insights that were done from previous policy code."
)
async def analyze_code():
    result = await get_all_findings()

    if not result:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not find any AI insights")

    return result




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
