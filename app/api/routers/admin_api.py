from fastapi import APIRouter, Depends

router = APIRouter()



@router.get(
    "/users/active",
    summary="Get Active Users",
    description="Get list of currently active users"
)
async def get_active_users():
    """
    Get list of users who have made requests recently.
    """
    # TODO: Implement user activity tracking
    return {
        "active_users": [],
        "total_active": 0,
        "time_window_minutes": 15
    }