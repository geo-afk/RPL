from app.api.services.resource_service import ResourceService
from fastapi import APIRouter, Depends, status

from app.api.services.roles_service import RoleService
from app.models.resource import Resource
from typing import Annotated

from app.models.role import Role

resource_router = APIRouter(
    prefix="/api",
    tags=["resource"],
)


def get_resource_service() -> ResourceService:
    return ResourceService()


def get_role_service() -> RoleService:
    return RoleService()



@resource_router.get(
    "/resource",
    status_code=status.HTTP_200_OK,
    response_model=list[Resource],
    summary="Get List of Resources",
    description="Returns all resources from the client_db.",
    tags=["Resources"]
)
async def receive_resources(
    service: Annotated[ResourceService, Depends(get_resource_service)]
):
    return await service.get_resources()


@resource_router.get(
    "/role",
    status_code=status.HTTP_200_OK,
    response_model=list[Role],
    summary="Get List of Roles",
    description="Returns all roles from the client_db.",
    tags=["Resources"]
)
async def receive_resources(
    service: Annotated[RoleService, Depends(get_role_service)]
):
    return service.get_roles()
