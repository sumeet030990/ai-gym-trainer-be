

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
    
    # 2. Define the tools your agent can use
    # (Ensure TAVILY_API_KEY is in your environment variables)
    tools = []

    # 3. Create the agent using create_agent
    # System prompt carries the persona, rules, and the client's static context
    # (profile, equipment, muscle list) — none of that changes mid-task. The
    # human message carries only the actual per-call request (the client's goals).
    if training_days:
        days_clause = (
            f"The client selected exactly these {len(training_days)} training days, in "
            f"this order: {training_days}. Generate exactly one workout day for each one "
            "— no more, no fewer — setting each day's `day` field to that exact label "
            "verbatim (e.g. \"Mon\") and keeping them in that same order. Do not add, "
            "drop, merge, reorder, or rename any day."
        )
    else:
        days_clause = (
            "Generate exactly one workout day for every training day per week the "
            "client stated in their goals."
        )

    system_prompt = (
        "You are an experienced, certified personal trainer creating a personalized "
        "workout plan for a client. Tailor the plan to their stated fitness goals, "
        "dietary preferences, and any health conditions they've shared, favoring safety "
        "over intensity when in doubt. Only use equipment confirmed to be available to "
        "the client; default to bodyweight exercises if equipment access is unknown or "
        f"empty. {days_clause} Each day should have one or two muscle groups and an "
        "ordered list of exercises, and include sets, reps, suggested weight in "
        "kilograms, and brief form cues for each exercise. Start weights conservatively "
        "(use 0 for bodyweight-only exercises) — weight will be progressed in future "
        "plans as the client's training history builds. For each workout day, set "
        f"muscles to a list of one or two closest matches from this exact list: "
        f"{muscle_names}. Decide as per the user_goals, if user should train single muscle"
        "or pair complementary muscle groups on the same day when the split calls for it"
        "use that pairing to cover as many distinct muscle groups across the "
        "week as the client's training frequency allows. Never target the same muscle "
        "group, alone or paired, on consecutive days, and do not repeat any muscle group "
        "anywhere in the week until every other muscle group used in this plan has "
        "appeared at least once — rotate through a coherent split (e.g. push/pull/legs, "
        "upper/lower, or full-body) appropriate to the client's training frequency and "
        "goal so each muscle gets at least 48 hours of recovery before it is trained "
        "again. For each exercise, set sort_order to "
        "reflect the sequence it should be performed in within its day, and include "
        "warm-up and, if appropriate for that muscle group, post-exercise stretches. Do "
        "not provide medical advice; if a condition suggests a client should consult a "
        "doctor before training, say so instead of prescribing exercises for it.\n\n"
        f"Client profile: {client_profile}\n"
        f"Available gym equipment: {equipment_names}\n"
         "Rules that must be followed while generating the plan:\n"
          "1. Decide the training split (single muscle vs. complementary muscle groups) based on the client's goals and training frequency. Mention your decision in note with reason\n"
          "2. Only use the provided muscle list and available equipment.\n"
          "3. Do not repeat any muscle group until all others have been trained.\n"
          "4. Ensure at least 48 hours of recovery for each muscle group before it is trained again.\n"
          "5. Provide warm-up and post-exercise stretches where appropriate.\n"
          "6. Do not provide medical advice; if a condition suggests a client should consult a doctor before training, say so instead of prescribing exercises for it.\n"
          "7. Ensure exercises are appropriate for the client's experience level and any existing injuries or limitations.\n"
          f"8. The `days` list must contain exactly one entry per client-selected training day{f' ({training_days})' if training_days else ''}, matched 1:1 in order — never a different count.\n"
    )

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
        response_format=WorkoutPlanSchema,
        debug=True # Enables detailed logging of the execution flow
    )

    agent_response = await agent.ainvoke({
      "messages": [
        HumanMessage(content=(
          "Create a personalized workout plan for this client. Based on the client's "
          "goals, decide whether they should focus on strength, hypertrophy, endurance, "
          "or a balanced approach, and whether each session should target a single "
          "muscle group or a pair of complementary muscle groups — reflect that decision "
          "in the plan and add it in notes.\n\n"
          f"Client goals: {user_goals}\n"
          f"Client's selected training days: {training_days}\n"
          "The `days` list must have exactly one entry per day listed above, in that "
          "order, with `day` set to that exact label."
        ))
      ]
    })

    workout_plan: WorkoutPlanSchema = agent_response["structured_response"]
    return workout_plan