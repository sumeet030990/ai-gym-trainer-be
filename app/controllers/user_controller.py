from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth_schemas import UserRegisterResponse, UserUpdateRequest
from app.schemas.common_schemas import PaginatedResponse, PaginationMeta
from app.schemas.user_goal_answers_schema import UserGoalAnswersRequestSchema
from app.services import user_service


async def get_all_users(db_session: AsyncSession, page: int = 1, page_size: int = 20) -> PaginatedResponse[UserRegisterResponse]:
    users, total_items = await user_service.get_all_users(db_session, page, page_size)
    total_pages = -(-total_items // page_size) if page_size else 0

    return PaginatedResponse(
        items=[UserRegisterResponse.model_validate(user) for user in users],
        meta=PaginationMeta(
            page=page,
            page_size=page_size,
            total_items=total_items,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_previous=page > 1,
        ),
    )

async def get_user_by_id(id: str, db_session: AsyncSession) -> UserRegisterResponse:
    user = await user_service.get_user_by_id(id, db_session)
    if not user:
        raise ValueError("User not found")
    return UserRegisterResponse.model_validate(user)

async def update_user_by_id(id: str, payload: UserUpdateRequest, db_session: AsyncSession) -> UserRegisterResponse:
    user = await user_service.update_user_by_id(id, payload, db_session)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return UserRegisterResponse.model_validate(user)

async def delete_user_by_id(id: str, db_session: AsyncSession) -> dict:
   result = await user_service.delete_user_by_id(id, db_session)
  
   return {"message": "User deleted successfully"}



async def update_user_goals(auth_user: UserRegisterResponse, payload: UserGoalAnswersRequestSchema, db_session: AsyncSession):
    user = await user_service.get_user_by_id(str(auth_user.id), db_session)
    if not user:
        raise ValueError("User not found")
    user = await user_service.update_user_goals(user, payload, db_session)
    return UserRegisterResponse.model_validate(user)
    