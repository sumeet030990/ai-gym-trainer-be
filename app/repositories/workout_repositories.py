
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.schemas.user_workout_plans import UserWorkoutPlans
from app.schemas.workout_plan_schema import WorkoutPlanSchema


async def save_workout_plan(user_details: dict, workout_plan: WorkoutPlanSchema, db_session: AsyncSession):
    user = user_details["user"]
    
    new_plan = UserWorkoutPlans(
        user_id=user.id,
        workout_plan=workout_plan.model_dump(mode="json")
    )
    
    db_session.add(new_plan)
    
    await db_session.commit()
    await db_session.refresh(new_plan)
    
    return new_plan
  
  
async def get_user_workout_plan(user_details: dict, db_session: AsyncSession) -> WorkoutPlanSchema:
    user = user_details["user"]
    
    result = await db_session.execute(
        select(UserWorkoutPlans).where(UserWorkoutPlans.user_id == user.id)
    )
    user_plan = result.scalars().first()
    
    if not user_plan:
        raise ValueError("Workout plan not found")
    
    return WorkoutPlanSchema.model_validate(user_plan.workout_plan)