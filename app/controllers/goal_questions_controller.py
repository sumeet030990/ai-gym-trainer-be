from app.schemas.goal_questions_schemas import CategoryResponse, GoalQuestionResponse, GoalQuestionOptionResponse, GoalQuestionsByCategoryResponse
from app.services import goal_questions_services

async def get_all_goal_questions(category_id: str|None, db_session):
    categories = await goal_questions_services.get_all_goal_questions(category_id, db_session)

    return [
        GoalQuestionsByCategoryResponse(
            category=CategoryResponse(id=category.id, name=category.name),
            questions=[
                GoalQuestionResponse(
                    id=question.id,
                    question=question.question,
                    question_type=question.question_type,
                    is_active=question.is_active,
                    category=CategoryResponse(id=category.id, name=category.name),
                    sort_order=question.sort_order,
                    options=[GoalQuestionOptionResponse(id=option.id, label=option.label, sort_order=option.sort_order) for option in question.options]
                )
                for question in category.questions
            ]
        )
        for category in categories
    ]