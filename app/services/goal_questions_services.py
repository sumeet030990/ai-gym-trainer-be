from app.repositories import categories_repository

async def get_all_goal_questions(category_id: str|None, db_session):
    return await categories_repository.get_all_categories_goal_questions(category_id, db_session)