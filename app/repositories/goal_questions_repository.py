
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from db.schemas import GoalQuestions, Categories

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