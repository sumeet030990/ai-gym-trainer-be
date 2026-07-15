
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from db.schemas import GoalQuestions

async def get_all_goal_questions(db_session: AsyncSession):
  total_items = await db_session.scalar(select(func.count()).select_from(GoalQuestions))
  
  statement = select(GoalQuestions)
  result = await db_session.scalars(statement)
  questions = result.all()

  return questions