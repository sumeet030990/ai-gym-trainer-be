from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers import auth_controllers
from app.schemas.auth_schemas import UserRegisterRequest, UserRegisterResponse
from db.database import get_session

router = APIRouter(tags=["Authentication"])


@router.post("/register", response_model=UserRegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(
    payload: UserRegisterRequest,
    db_session: AsyncSession = Depends(get_session),
) -> UserRegisterResponse:
    return await auth_controllers.register(payload, db_session)
