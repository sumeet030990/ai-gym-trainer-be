
from core.security import is_user_authenticated
from db.database import get_session
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.controllers import equipments_controller

router = APIRouter(
    prefix="/equipments",
    tags=["equipments"],
)


@router.get("/")
async def get_all_equipments(page: int = 1, page_size: int = 10, auth_user=Depends(is_user_authenticated), db_session=Depends(get_session)):
  return await equipments_controller.get_all_equipments(db_session, page, page_size)
