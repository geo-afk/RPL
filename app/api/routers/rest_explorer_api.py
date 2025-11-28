from fastapi import status, APIRouter
from typing import List
from app.api.routers.mock_api import mock_router
from app.api.services.rest_service import extract_router_routes, RouteInfo

rest_router = APIRouter(
    prefix="/rest",
    tags=["Rest"],
)



@rest_router.get(
    "/api/endpoints",
    status_code=status.HTTP_201_CREATED,
    response_model=List[RouteInfo],
    summary="All Mock endpoint for client",
    description="Retrieve all the mock endpoints for client."
)
async def endpoints():
    return extract_router_routes(mock_router)
