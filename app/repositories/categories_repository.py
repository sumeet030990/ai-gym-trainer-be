
from db.schemas.categories import Categories
from db.schemas.goal_questions import GoalQuestions
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Sequence


async def get_all_categories_goal_questions(category_id: str|None, db_session: AsyncSession) -> Sequence[Categories]:
  """Returns categories with their active goal questions eager-loaded, grouped by category."""
  statement = (
    select(Categories)
    .options(
      selectinload(
        Categories.questions.and_(GoalQuestions.is_active == True)
      ).selectinload(GoalQuestions.options),
    )
    .order_by(Categories.sort_order)
    .where(Categories.name != "Medical & Injury")  # Exclude the "Medical & Injury" category
    .where(Categories.questions.any(GoalQuestions.is_active == True))  # Drop categories with no active questions
  )

  if category_id:
    statement = statement.where(Categories.id == category_id)

  result = await db_session.execute(statement)

  return result.scalars().all()