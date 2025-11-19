from app.api.services.resource_service import ResourceService
from fastapi import APIRouter, Depends, status
from app.models.resourse import Resource
from typing import Annotated

router = APIRouter()


def get_resource_service() -> ResourceService:
    return ResourceService()


@router.get(
    "/resource",
    status_code=status.HTTP_200_OK,
    response_model=list[Resource],
    summary="Get List of Resources",
    description="Returns all resources from the database.",
    tags=["Resources"]
)
async def receive_resources(
    service: Annotated[ResourceService, Depends(get_resource_service)]
):
    return await service.get_resources()
