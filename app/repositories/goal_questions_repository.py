import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from db.schemas import GoalQuestions, GoalQuestionOptions, Categories

async def get_all_goal_questions(category_id: str|None, db_session: AsyncSession):
  statement = (
    select(GoalQuestions)
    .options(
      selectinload(GoalQuestions.options),
      joinedload(GoalQuestions.category),
    )
    .order_by(GoalQuestions.sort_order)
    .where(GoalQuestions.is_active == True)
  )
  
  if category_id:
    statement = statement.where(GoalQuestions.category_id == category_id)
  
  result = await db_session.execute(statement)

  return result.scalars().all()

async def get_goal_question_by_id(db_session: AsyncSession, question_id: uuid.UUID) -> GoalQuestions | None:
  result = await db_session.execute(select(GoalQuestions).where(GoalQuestions.id == question_id))
  return result.scalar_one_or_none()

async def get_goal_question_option_by_id(db_session: AsyncSession, option_id: uuid.UUID) -> GoalQuestionOptions | None:
  result = await db_session.execute(select(GoalQuestionOptions).where(GoalQuestionOptions.id == option_id))
  return result.scalar_one_or_none()