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
