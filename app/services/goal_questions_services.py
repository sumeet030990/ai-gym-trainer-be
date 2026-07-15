from app.repositories import goal_questions_repository

async def get_all_goal_questions(db_session):
    return await goal_questions_repository.get_all_goal_questions(db_session)