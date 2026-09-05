
from datetime import date, datetime, time, timezone, timedelta
import uuid
from uuid import UUID
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.workout_schemas import WorkoutLogRequest
from db.schemas.user_workout_plans import UserWorkoutPlans
from db.schemas.user_attendance import UserAttendance
from db.schemas.workout_logs import WorkoutLogs
from db.schemas.workout_log_exercises import WorkoutLogExercises
from db.schemas.workout_log_sets import WorkoutLogSets
from app.schemas.workout_plan_schema import WorkoutPlanResponseSchema, WorkoutPlanSchema, GetUserWorkoutPlanResponseSchema


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
  
  
async def get_user_workout_plan(user_id: UUID, db_session: AsyncSession) -> WorkoutPlanResponseSchema:
    
    result = await db_session.execute(
        select(UserWorkoutPlans).where(UserWorkoutPlans.user_id == user_id).order_by(UserWorkoutPlans.created_at.desc())
    )
    user_plan = result.scalars().first()
    
    if not user_plan:
        raise ValueError("Workout plan not found")
    
    return WorkoutPlanResponseSchema.model_validate(user_plan)


async def get_user_workout_logs(userId: UUID, db_session: AsyncSession, start_date: Optional[str] = None, end_date: Optional[str] = None):
    query = (
        select(WorkoutLogs, UserAttendance.attendance_date)
        .join(UserAttendance, WorkoutLogs.attendance_id == UserAttendance.id)
        .where(WorkoutLogs.user_id == userId)
    )

    if start_date:
        start_of_day = datetime.combine(date.fromisoformat(start_date), time.min)
        query = query.where(UserAttendance.attendance_date >= start_of_day)
    else:
        # attendance_date is stored as a naive UTC timestamp (see attendance_repository.create_attendance)
        thirty_days_ago = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=30)
        query = query.where(UserAttendance.attendance_date >= thirty_days_ago)
    if end_date:
        end_of_day = datetime.combine(date.fromisoformat(end_date), time.max)
        query = query.where(UserAttendance.attendance_date <= end_of_day)
    else:
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        query = query.where(UserAttendance.attendance_date <= now)

    result = await db_session.execute(query.order_by(UserAttendance.attendance_date.desc()))
    data = result.all()

    return [
        GetUserWorkoutPlanResponseSchema(
            id=log.id,
            workout_date=attendance_date,
            created_at=log.created_at,
        )
        for log, attendance_date in data
    ]

async def log_workout(userId: UUID, workout_log: WorkoutLogRequest, db_session: AsyncSession) -> WorkoutLogs:
    new_log = WorkoutLogs(
        id=uuid.uuid4(),
        user_id=userId,
        attendance_id=workout_log.attendance_id,
    )
    db_session.add(new_log)
    # No ORM relationship() ties these tables together (only raw FK columns), so the
    # unit-of-work can't infer insert order on its own — flush the parent before adding
    # rows that reference it, or the child INSERTs can be emitted first and violate the FK.
    await db_session.flush()

    new_exercises = []
    for muscle_log in workout_log.muscles:
        for exercise_log in muscle_log.exercises:
            new_exercise = WorkoutLogExercises(
                id=uuid.uuid4(),
                workout_log_id=new_log.id,
                muscle_id=muscle_log.muscle_id,
                exercise_id=exercise_log.exercise_id,
            )
            db_session.add(new_exercise)
            new_exercises.append((new_exercise, exercise_log.sets))

    await db_session.flush()

    for new_exercise, sets in new_exercises:
        for set_log in sets:
            db_session.add(WorkoutLogSets(
                id=uuid.uuid4(),
                workout_log_exercise_id=new_exercise.id,
                set_number=set_log.set_number,
                reps=set_log.reps,
                weight_kg=set_log.weight_kg,
            ))

    await db_session.commit()
    await db_session.refresh(new_log)

    return new_log