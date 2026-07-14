from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth_schemas import UserRegisterResponse
from app.schemas.common_schemas import PaginatedResponse, PaginationMeta
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