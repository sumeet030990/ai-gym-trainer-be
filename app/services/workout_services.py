from app.schemas.workout_schemas import WorkoutLogRequest
from app.services import equipments_services, muscle_services
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from ai.agent import get_llm_provider
from app.schemas.workout_plan_schema import WorkoutPlanResponseSchema, WorkoutPlanSchema
import os
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from app.repositories import workout_repositories
from uuid import UUID

async def get_user_goals(user_details: dict):
  user_goals = []
  for goal in user_details["user_goals"]:
      answers = [
          answer.option.label if answer.option is not None else answer.answer_text
          for answer in goal.answers
      ]
      user_goals.append({
          "question": goal.question.question,
          "answers": answers,
      })
  return user_goals

async def get_user_age(user):
  today = date.today()
  age = None
  if user.birth_date:
      age = today.year - user.birth_date.year - (
          (today.month, today.day) < (user.birth_date.month, user.birth_date.day)
      )
  return age
  
  
async def get_gym_context(db_session: AsyncSession):
  gym_equipment = await equipments_services.get_all_equipments(db_session, page=1, page_size=10)
  muscles = await muscle_services.get_all_muscles(db_session)
  return (
      [equipment.name for equipment in gym_equipment],
      [muscle.name for muscle in muscles],
  )


def get_training_days(user_goals: list[dict]) -> list:
  # Pulled out explicitly (rather than left for the LLM to notice inside the
  # full user_goals list) so the plan's day count/labels are guaranteed to
  # match what the client picked, instead of the model inferring/recounting
  # training days from free-text goals.
  return next(
      (goal["answers"] for goal in user_goals if goal["question"] == "Which days work best for you?"),
      [],
  )


def get_latest_measurement(user):
  return max(user.body_measurements, key=lambda m: m.created_at, default=None)


def build_workout_llm_agent():
  # TODO: later as per user preferences will use llm and model.
  llm = get_llm_provider(apiKey=str(os.getenv("GROQ_API_KEY")), llm_name="groq", model_name="openai/gpt-oss-120b")

  return create_agent(
      model=llm,
      tools=[],
      system_prompt=build_workout_plan_system_prompt(),
      response_format=WorkoutPlanSchema,
      debug=True # Enables detailed logging of the execution flow
  )


def build_workout_plan_system_prompt() -> str:
  # Kept terse: every extra sentence here is billed on every request against
  # Groq's on-demand TPM budget for this model (see ai/providers/groq.py).
  return (
      "You are a certified personal trainer creating a personalized workout plan. "
      "Follow the client's stated training days strictly. "
      "Choose single-muscle or double-muscle based on their goal and training frequency; explain the choice in plan notes. "
      "As per the selected muscle groups, choose exercises that can be performed with the available equipment. "
      "Don't suggest exercises that require equipment the user doesn't have. "
      "Don't repeat a muscle group until all others have been trained that week, unless the goal requires it. "
      "Start weights conservatively (0 for bodyweight exercises). "
      "For each day give targeted muscles, an ordered list of exercises, sets, reps, suggested weight in kg, and a brief form cue per exercise. "
      "Suggest warm-up as per the muscles trained that day. "
      "Suggest a post-exercise stretch routine as per the muscles trained that day; leave it empty only if stretching isn't appropriate. "
      "For any health condition, suggest modifications or alternative exercises, or skip muscle targeting if needed for safety, and note it. "
      "Keep all notes brief."
  )


def build_workout_plan_prompt(
    user, age, latest_measurement, user_goals, muscle_names, equipment_names, training_days
) -> str:
  # Only fitness-relevant fields are sent to the LLM — never PII like email,
  # mobile number, raw birth date, or the password hash from the `user` ORM
  # object. Age is derived from birth_date rather than sending the date itself.
  return (
      "Create a personalized workout plan for the user with details.\n"
      f"name: {user.first_name} {user.last_name}\n"
      f"gender: {user.sex}\n"
      f"age: {age}\n"
      f"dietary preferences: {user.diet_type}\n"
      f"user current weight: {latest_measurement.weight_kg if latest_measurement else 'Not Available'} kg\n"
      f"user current height: {latest_measurement.height_cm if latest_measurement else 'Not Available'} cm\n"
      f"user current body fat percentage: {latest_measurement.body_fat_percent if latest_measurement else 'Not Available'}%\n"
      f"User goals: {user_goals}\n"
      f"Suggest exercises targeting these muscles only: {muscle_names}.\n"
      f"Equipment available to the user: {equipment_names}.\n"
      f"User will train on these days: {training_days}\n"
  )


async def generate_workout_plan(user_details: dict, db_session: AsyncSession) -> WorkoutPlanSchema:
  user = user_details["user"]

  equipment_names, muscle_names = await get_gym_context(db_session)
  user_goals = await get_user_goals(user_details)
  training_days = get_training_days(user_goals)
  age = await get_user_age(user)
  latest_measurement = get_latest_measurement(user)

  agent = build_workout_llm_agent()
  prompt = build_workout_plan_prompt(
      user, age, latest_measurement, user_goals, muscle_names, equipment_names, training_days
  )

  agent_response = await agent.ainvoke({
      "messages": [
          HumanMessage(content=prompt)
      ]
  })

  return agent_response["structured_response"]



# =====================================


async def save_workout_plan(user_details: dict, workout_plan: WorkoutPlanSchema, db_session: AsyncSession):
  return await workout_repositories.save_workout_plan(user_details, workout_plan, db_session)

async def get_user_workout_plan(user_id: UUID, db_session: AsyncSession) -> WorkoutPlanResponseSchema:
  return await workout_repositories.get_user_workout_plan(user_id, db_session)


async def check_if_workout_plan_regeneration_needed(userId: UUID, db_session: AsyncSession) -> bool:
  try:
      
      user_workout_plan = await workout_repositories.get_user_workout_plan(userId, db_session)
      if not user_workout_plan:
          return True
      # Check if the workout plan needs regeneration based on custom logic
      # For now, we assume it doesn't need regeneration if it exists
      
      return False
  except ValueError:
      return True
    
    
# =====================================
async def log_workout(userId: UUID, workout_log: WorkoutLogRequest, db_session: AsyncSession):
  return await workout_repositories.log_workout(userId, workout_log, db_session)