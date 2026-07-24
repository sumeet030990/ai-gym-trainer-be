from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers import auth_controller
from app.schemas.auth_schemas import UserLoginRequest, UserRegisterRequest, UserRegisterResponse
from db.database import get_session

router = APIRouter(tags=["Authentication"])


@router.post("/register", response_model=UserRegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(
    payload: UserRegisterRequest,
    db_session: AsyncSession = Depends(get_session),
) -> UserRegisterResponse:
    return await auth_controller.register(payload, db_session)


@router.post("/login")
async def login(payload: UserLoginRequest, db_session: AsyncSession = Depends(get_session)):
    return await auth_controller.login(payload, db_session)