import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from db.schemas import GoalQuestions, GoalQuestionOptions, Categories

async def get_all_goal_questions(db_session: AsyncSession):
  statement = (
    select(GoalQuestions, Categories)
    .outerjoin(Categories, GoalQuestions.category == Categories.id)
    .options(selectinload(GoalQuestions.options))
    .order_by(GoalQuestions.sort_order)
    .where(GoalQuestions.is_active == True)
  )
  result = await db_session.execute(statement)

  return result.all()

async def get_goal_question_by_id(db_session: AsyncSession, question_id: uuid.UUID) -> GoalQuestions | None:
  result = await db_session.execute(select(GoalQuestions).where(GoalQuestions.id == question_id))
  return result.scalar_one_or_none()

async def get_goal_question_option_by_id(db_session: AsyncSession, option_id: uuid.UUID) -> GoalQuestionOptions | None:
  result = await db_session.execute(select(GoalQuestionOptions).where(GoalQuestionOptions.id == option_id))
  return result.scalar_one_or_none()