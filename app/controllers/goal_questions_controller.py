from app.schemas.goal_questions_schemas import CategoryResponse, GoalQuestionResponse,GoalQuestionOptionResponse
from app.services import goal_questions_services

async def get_all_goal_questions(db_session):
    rows = await goal_questions_services.get_all_goal_questions(db_session)
    return [
        GoalQuestionResponse(
            id=question.id,
            question=question.question,
            question_type=question.question_type,
            is_active=question.is_active,
            category=CategoryResponse(id=category.id, name=category.name) if category else None,
            sort_order=question.sort_order,
            options=[GoalQuestionOptionResponse(id=option.id, label=option.label, sort_order=option.sort_order) for option in question.options]
        )
        for question, category in rows
    ]