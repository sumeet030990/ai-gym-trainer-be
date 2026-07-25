from fastapi import APIRouter, Depends

from app.controllers import gyms_controller
from core.security import is_user_authenticated
from db.database import get_session

router = APIRouter(
    prefix="/gyms",
    tags=["gyms"],
)


@router.get("/")
async def get_all_gyms(page: int = 1, page_size: int = 10, auth_user=Depends(is_user_authenticated), db_session=Depends(get_session)):
    return await gyms_controller.get_all_gyms(db_session, page, page_size)

@router.get("/{gym_id}")
async def get_gym_by_id(gym_id: str, auth_user=Depends(is_user_authenticated), db_session=Depends(get_session)):
    return await gyms_controller.get_gym_by_id(gym_id, db_session)

@router.post("/")
async def create_gym(gym_data: dict, auth_user=Depends(is_user_authenticated), db_session=Depends(get_session)):
    return await gyms_controller.create_gym(gym_data, db_session)

@router.put("/{gym_id}")
async def update_gym(gym_id: str, gym_data: dict, auth_user=Depends(is_user_authenticated), db_session=Depends(get_session)):
    return await gyms_controller.update_gym(gym_id, gym_data, db_session)


@router.delete("/{gym_id}")
async def delete_gym(gym_id: str, auth_user=Depends(is_user_authenticated), db_session=Depends(get_session)):
    return await gyms_controller.delete_gym(gym_id, db_session)


@router.get("/{gym_id}/users")
async def get_gym_users(gym_id: str, user_role_id: str | None = None, auth_user=Depends(is_user_authenticated), db_session=Depends(get_session)):
    return await gyms_controller.get_gym_users(gym_id, user_role_id, db_session)