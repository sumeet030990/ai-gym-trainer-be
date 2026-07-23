from app.repositories import goal_questions_repository

async def get_all_goal_questions(category_id: str|None, db_session):
    return await goal_questions_repository.get_all_goal_questions(category_id, db_session)