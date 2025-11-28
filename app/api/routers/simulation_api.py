from starlette import status

from app.api.services.simulation_service import check_user_permissions
from app.models.auth_models import Token
from fastapi import APIRouter, HTTPException

from app.models.response.simulation_response import PermissionCheck

simulation_router = APIRouter(
    prefix="/api",
    tags=["Simulation"],
)


@simulation_router.get(
    path="/simulation",
    response_model=PermissionCheck,
    status_code=status.HTTP_200_OK,
    summary="Check user permissions",
    description="Check if the user is expired, then check the users permissions to resources",
)
async def simulation(token: Token):
    response = check_user_permissions(token)

    if not response:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User simulation check failed, user expired")

    return response

