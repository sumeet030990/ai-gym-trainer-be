

from datetime import date

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

from ai.agent import get_llm_provider
from app.schemas.auth_schemas import UserRegisterResponse
from app.schemas.workout_plan_schema import WorkoutPlanSchema
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import equipments_services, user_services, muscle_services
import os



async def generate_plan(auth_user: UserRegisterResponse, db_session: AsyncSession):
    """Generate a personalized workout plan based on user goals and preferences."""
    user_details = await user_services.get_auth_user_details(auth_user, db_session)

    if not user_details:
        raise ValueError("User not found")

    user = user_details["user"]

    gym_equipment = await equipments_services.get_all_equipments(db_session, page=1, page_size=10)
    equipment_names = [equipment.name for equipment in gym_equipment]
    muscles = await muscle_services.get_all_muscles(db_session)
    muscle_names = [muscle.name for muscle in muscles]

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

    # Pulled out explicitly (rather than left for the LLM to notice inside the
    # full user_goals list) so the plan's day count/labels are guaranteed to
    # match what the client picked, instead of the model inferring/recounting
    # training days from free-text goals.
    training_days = next(
        (goal["answers"] for goal in user_goals if goal["question"] == "Which days work best for you?"),
        [],
    )

    # Only fitness-relevant fields are sent to the LLM — never PII like email,
    # mobile number, raw birth date, or the password hash from the `user` ORM
    # object. Age is derived from birth_date rather than sending the date itself.
    today = date.today()
    age = None
    if user.birth_date:
        age = today.year - user.birth_date.year - (
            (today.month, today.day) < (user.birth_date.month, user.birth_date.day)
        )

    latest_measurement = max(
        user.body_measurements, key=lambda m: m.created_at, default=None
    )
    client_profile = {
        "age": age,
        "sex": user.sex.value if user.sex else None,
        "diet_type": user.diet_type.value if user.diet_type else None,
        "health_conditions": [
            {"condition": condition.condition_name, "notes": condition.notes}
            for condition in user.health_conditions
        ],
        "body_measurements": (
            {
                "weight_kg": latest_measurement.weight_kg,
                "height_cm": latest_measurement.height_cm,
                "body_fat_percent": latest_measurement.body_fat_percent,
            }
            if latest_measurement
            else None
        ),
    }

    # TODO: later as per user preferences will use llm and model.
    llm = get_llm_provider(apiKey=str(os.getenv("GROQ_API_KEY")), llm_name="groq", model_name="openai/gpt-oss-120b")

    tools = []

    # Kept terse: every extra sentence here is billed on every request against
    # Groq's on-demand TPM budget for this model (see ai/providers/groq.py).
    sys_prompt = (
        "You are a certified personal trainer creating a personalized workout plan. "
        "Follow the client's stated training days strictly. "
        "Choose single-muscle or double-muscle based on their goal and training frequency; explain the choice in plan notes. "
        "As per the selected muscle groups, choose exercises that can be performed with the available equipment. "
        "Don't suggest exercises that require equipment the user doesn't have. "
        "Don't repeat a muscle group until all others have been trained that week, unless the goal requires it. "
        "Start weights conservatively (0 for bodyweight exercises). "
        "For each day give targeted muscles, an ordered list of exercises, sets, reps, suggested weight in kg, and a brief form cue per exercise. "
        "Suggest warm-up as per the muscles trained that day. "
        "For any health condition, suggest modifications or alternative exercises, or skip muscle targeting if needed for safety, and note it. "
        "Keep all notes brief."
    )

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=sys_prompt,
        response_format=WorkoutPlanSchema,
        debug=True # Enables detailed logging of the execution flow
    )

    humanMessage = (
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
    agent_response = await agent.ainvoke({
        "messages": [
            HumanMessage(content=humanMessage)
        ]
    })

    workout_plan: WorkoutPlanSchema = agent_response["structured_response"]
    return workout_plan