from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import user_repository, auth_repository, goal_questions_repository
from app.schemas.auth_schemas import UserUpdateRequest
from app.schemas.user_goal_answers_schema import UserGoalAnswersRequestSchema
from db.database import get_session


async def get_all_users(db_session: AsyncSession, page: int, page_size: int):
    return await user_repository.get_all_users(db_session, page, page_size)

async def get_user_by_mobile_or_email(user_name: str, db_session: AsyncSession = Depends(get_session)):
    return await auth_repository.get_by_mobile_or_email(db_session, user_name)

async def get_user_by_id(id: str, db_session: AsyncSession):
    return await user_repository.get_user_by_id(db_session, id)


async def update_user_by_id(id: str, payload: UserUpdateRequest, db_session: AsyncSession):
    user = await user_repository.get_user_by_id(db_session, id)
    if not user:
        return None

    update_data = payload.model_dump(exclude_unset=True)

    if "mobile_no" in update_data and update_data["mobile_no"] != user.mobile_no:
        existing = await auth_repository.get_by_mobile_no(db_session, update_data["mobile_no"])
        if existing is not None and existing.id != user.id:
            raise HTTPException(status.HTTP_409_CONFLICT, "Mobile number is already registered.")

    if "email" in update_data and update_data["email"] is not None and update_data["email"] != user.email:
        existing = await auth_repository.get_by_email(db_session, update_data["email"])
        if existing is not None and existing.id != user.id:
            raise HTTPException(status.HTTP_409_CONFLICT, "Email is already registered.")

    for field, value in update_data.items():
        setattr(user, field, value)

    return await user_repository.update_user(db_session, user)


async def delete_user_by_id(id: str, db_session: AsyncSession):
    user = await user_repository.get_user_by_id(db_session, id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    
    result = await user_repository.delete_user(db_session, user)
    return result



async def update_user_goals(user, payload: UserGoalAnswersRequestSchema, db_session: AsyncSession):
    question = await goal_questions_repository.get_goal_question_by_id(db_session, payload.question_id)
    if not question:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Goal question not found")

    await user_repository.save_user_goal_answers(
        db_session,
        user.id,
        payload.question_id,
        [(answer.option_id, answer.answer_text) for answer in payload.answers],
    )

    return user

 