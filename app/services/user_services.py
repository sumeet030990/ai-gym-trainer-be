import json
from collections import defaultdict

from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import user_repository, auth_repository
from app.schemas.auth_schemas import UserRegisterResponse, UserUpdateRequest
from app.schemas.user_goal_answers_schema import UserGoalAnswerGroupSchema, UserGoalAnswersRequestSchema
from db.database import get_session
from db.schemas.user_goal_answer import UserGoalAnswers


async def get_all_users(db_session: AsyncSession, page: int, page_size: int):
    return await user_repository.get_all_users(db_session, page, page_size)

async def get_user_by_mobile_or_email(user_name: str, db_session: AsyncSession = Depends(get_session)):
    return await auth_repository.get_by_mobile_or_email(db_session, user_name)

async def get_user_by_id(id: str, db_session: AsyncSession):
    return await user_repository.get_user_by_id(db_session, id)

async def get_auth_user_details(auth_user: UserRegisterResponse, db_session: AsyncSession):
    usr =  await user_repository.get_auth_user_details(db_session, str(auth_user.id))
    if not usr:
        raise ValueError("User not found")
    user_goals = await get_user_goals(auth_user, db_session)
    return {"user": usr, "user_goals": user_goals}


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


async def get_user_goals(auth_user: UserRegisterResponse, db_session: AsyncSession)-> list[UserGoalAnswerGroupSchema]:
    answers = await user_repository.get_user_goals(db_session, auth_user.id)

    grouped = defaultdict(list)
    for answer in answers:
        grouped[answer.question_id].append(answer)

    return [
        UserGoalAnswerGroupSchema.model_validate(
            {"question": question_answers[0].question, "answers": question_answers}
        )
        for question_answers in grouped.values()
    ]


async def update_user_goals(user, payload: UserGoalAnswersRequestSchema, db_session: AsyncSession) -> list[UserGoalAnswers]:
    data = [
        {
            "user_id": user.id,
            "question_id": question.question_id,
            "option_id": answer.option_id,
            "answer_text": answer.answer_text,
        }
        for question in payload.user_goals
        for answer in question.answers
    ]

    result = await user_repository.save_user_goal_answers(
        db_session,
        user.id,
        data
    )
    
    return result

async def delete_user_goal_answers(user, db_session: AsyncSession) -> bool:
    result = await user_repository.delete_user_goal_answers(db_session, user.id)
    return result

async def get_gym_users(gym_id: str, user_role_id: str | None, db_session: AsyncSession):
    return await user_repository.get_gym_users(gym_id, user_role_id, db_session)