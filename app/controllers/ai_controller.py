

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

from ai.agent import get_llm_provider
from app.schemas.auth_schemas import UserRegisterResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import user_services
import os



async def generate_plan(auth_user: UserRegisterResponse, db_session: AsyncSession):
    """Generate a personalized workout plan based on user goals and preferences."""
    user = await user_services.get_auth_user_details(auth_user, db_session)
    if not user:
        raise ValueError("User not found")
    
    user_goals = []
    for goal in user["user_goals"]:
        answers = [
            answer.option.label if answer.option is not None else answer.answer_text
            for answer in goal.answers
        ]
        user_goals.append({
            "question": goal.question.question,
            "answers": answers,
        })

    # TODO: later as per user preferences will use llm and model.
    llm = get_llm_provider(apiKey=str(os.getenv("GROQ_API_KEY")), llm_name="groq", model_name="openai/gpt-oss-120b")
    
    # 2. Define the tools your agent can use
    # (Ensure TAVILY_API_KEY is in your environment variables)
    tools = []

    # 3. Create the agent using create_agent
    # Instead of a complex prompt template payload, pass instructions via system_prompt
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=(
            "You are an experienced, certified personal trainer creating a personalized "
            "workout plan for a client. Tailor the plan to their stated fitness goals, "
            "activity/experience level, dietary preferences, and any health conditions or "
            "physical limitations they've shared, favoring safety over intensity when in doubt. "
            "Only use equipment confirmed to be available to the client; default to bodyweight "
            "exercises if equipment access is unknown. Structure the plan with a warm-up, the "
            "main workout (split by day if multi-day), and a cool-down, and include sets, reps, "
            "rest periods, and brief form cues for each exercise. Do not provide medical advice; "
            "if a condition suggests a client should consult a doctor before training, say so "
            "instead of prescribing exercises for it."
        ),
        debug=True # Enables detailed logging of the execution flow
    )
    
    agent_response = agent.invoke({
      "messages": [
        HumanMessage(content=(
            f"Create a personalized workout plan for a client with the the user goals mentioned in api: {user_goals} "
        ))
      ]
    })
    
    return agent_response["messages"][-1].content