from app.services import goal_questions_services

async def get_all_goal_questions(db_session):
    return await goal_questions_services.get_all_goal_questions(db_session)