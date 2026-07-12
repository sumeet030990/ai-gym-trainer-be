from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth_schemas import UserRegisterRequest, UserRegisterResponse
from app.services import auth_services


async def register(payload: UserRegisterRequest, db_session: AsyncSession) -> UserRegisterResponse:
    user = await auth_services.register(payload, db_session)
    
    return UserRegisterResponse.model_validate(user)
