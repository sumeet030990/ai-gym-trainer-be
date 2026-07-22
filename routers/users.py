from fastapi import APIRouter, Depends, Query
from app.controllers import user_controller
from app.schemas.auth_schemas import UserRegisterResponse, UserUpdateRequest
from app.schemas.user_goal_answers_schema import UserGoalAnswersRequestSchema
from app.schemas.common_schemas import PaginatedResponse
from core.security import is_user_authenticated
from db.database import get_session

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=PaginatedResponse[UserRegisterResponse])
async def get_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    auth_user=Depends(is_user_authenticated),
    db_session=Depends(get_session),
):
    return await user_controller.get_all_users(db_session, page, page_size)

@router.get("/{id}", response_model=UserRegisterResponse)
async def get_user_by_id(id: str, auth_user=Depends(is_user_authenticated), db_session=Depends(get_session)):
    return await user_controller.get_user_by_id(id,db_session)


@router.put("/{id}", response_model=UserRegisterResponse)
async def update_user_by_id(
    id: str,
    payload: UserUpdateRequest,
    auth_user=Depends(is_user_authenticated),
    db_session=Depends(get_session),
):
    return await user_controller.update_user_by_id(id, payload, db_session)


@router.delete("/{id}")
async def delete_user_by_id(id: str, auth_user=Depends(is_user_authenticated), db_session=Depends(get_session)):
    return await user_controller.delete_user_by_id(id, db_session)


@router.post("/profile/goals")
async def update_user_goals(
    payload: UserGoalAnswersRequestSchema,
    auth_user=Depends(is_user_authenticated),
    db_session=Depends(get_session),
):
    return await user_controller.update_user_goals(auth_user, payload, db_session)

@router.delete("/profile/goals")
async def delete_user_goal_answers(
    auth_user=Depends(is_user_authenticated),
    db_session=Depends(get_session),
):
    return await user_controller.delete_user_goal_answers(auth_user, db_session)