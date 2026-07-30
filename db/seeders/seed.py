"""Idempotent database seeder for initial reference data.

Run with:
    uv run python -m db.seeders.seed
"""
import asyncio
from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import hash_password
from db.database import Async_session
from db.schemas import (
    AiModels,
    AiProviders,
    Categories,
    Equipments,
    Exercises,
    ExerciseEquipment,
    GoalQuestionOptions,
    GoalQuestions,
    GymEquipments,
    Gyms,
    Muscles,
    Roles,
    UserConditions,
    UserGoalAnswers,
    Users,
)
from db.schemas.exercises import LEVEL
from db.schemas.goal_questions import QUESTION_TYPE
from db.schemas.users import DietType
from db.seeders.seed_data import (
    AI_PROVIDERS,
    CATEGORIES,
    EQUIPMENT,
    EXERCISES,
    GOAL_QUESTIONS,
    GYMS,
    MUSCLES,
    ROLES,
    USER_CONDITIONS,
    USER_GOAL_ANSWERS,
    USERS,
)


async def _get_or_create(session: AsyncSession, model, defaults: dict | None = None, **filters):
    stmt = select(model).filter_by(**filters)
    existing = (await session.execute(stmt)).scalar_one_or_none()
    if existing is not None:
        return existing, False

    instance = model(**filters, **(defaults or {}))
    session.add(instance)
    await session.flush()
    return instance, True


async def seed_roles(session: AsyncSession) -> dict[str, Roles]:
    roles = {}
    for name in ROLES:
        role, _ = await _get_or_create(session, Roles, name=name)
        roles[name] = role
    return roles


async def seed_muscles(session: AsyncSession) -> dict[str, Muscles]:
    muscles = {}
    for name in MUSCLES:
        muscle, _ = await _get_or_create(session, Muscles, name=name)
        muscles[name] = muscle
    return muscles


async def seed_categories(session: AsyncSession) -> dict[str, Categories]:
    categories = {}
    for sort_order, name in enumerate(CATEGORIES, start=1):
        category, _ = await _get_or_create(session, Categories, name=name, defaults={"sort_order": sort_order})
        categories[name] = category
    return categories


async def seed_ai_catalog(session: AsyncSession) -> None:
    for provider_name, model_names in AI_PROVIDERS.items():
        provider, _ = await _get_or_create(session, AiProviders, name=provider_name)
        for model_name in model_names:
            await _get_or_create(session, AiModels, name=model_name, ai_provider_id=provider.id)


async def seed_gyms(session: AsyncSession, users: dict[str, Users]) -> dict[str, Gyms]:
    gyms = {}
    for gym_data in GYMS:
        owner_email = gym_data.get("owner_email")
        owner = users[owner_email] if owner_email else None
        gym, _ = await _get_or_create(
            session,
            Gyms,
            name=gym_data["name"],
            defaults={
                "location": gym_data["location"],
                "owner_user_id": owner.id if owner else None,
            },
        )
        gyms[gym.name] = gym
    return gyms


async def seed_equipment_catalog(session: AsyncSession) -> dict[str, Equipments]:
    catalog = {}
    for name, description in EQUIPMENT:
        item, _ = await _get_or_create(session, Equipments, name=name, defaults={"description": description})
        catalog[name] = item
    return catalog


async def seed_gym_equipment(
    session: AsyncSession,
    gym: Gyms,
    equipment_catalog: dict[str, Equipments],
) -> dict[str, GymEquipments]:
    gym_equipment = {}
    for name, equipment in equipment_catalog.items():
        item, _ = await _get_or_create(session, GymEquipments, gym_id=gym.id, equipment_id=equipment.id)
        gym_equipment[name] = item
    return gym_equipment


async def seed_exercises(
    session: AsyncSession,
    muscles: dict[str, Muscles],
    gym_equipment: dict[str, GymEquipments],
) -> None:
    for name, description, muscle_name, primary_equipment_name, extra_equipment_names, level in EXERCISES:
        muscle = muscles[muscle_name]
        primary_equipment = gym_equipment[primary_equipment_name] if primary_equipment_name else None

        exercise, _ = await _get_or_create(
            session,
            Exercises,
            name=name,
            defaults={
                "description": description,
                "muscle_id": muscle.id,
                "equipment_id": primary_equipment.id if primary_equipment else None,
                "excercise_level": LEVEL(level),
            },
        )

        for extra_name in extra_equipment_names:
            extra_equipment = gym_equipment[extra_name]
            await _get_or_create(
                session,
                ExerciseEquipment,
                exercise_id=exercise.id,
                equipment_id=extra_equipment.id,
            )


async def seed_users(session: AsyncSession, roles: dict[str, Roles]) -> dict[str, Users]:
    users = {}
    for user_data in USERS:
        role = roles[user_data["role_name"]]
        user, _ = await _get_or_create(
            session,
            Users,
            mobile_no=user_data["mobile_no"],
            defaults={
                "role_id": role.id,
                "email": user_data["email"],
                "password": hash_password(user_data["password"]),
                "first_name": user_data["first_name"],
                "last_name": user_data["last_name"],
                "birth_date": date.fromisoformat(user_data["birth_date"]),
                "sex": user_data["sex"],
                "diet_type": DietType(user_data["diet_type"]),
            },
        )
        users[user.email] = user
    return users


async def seed_goal_questions(
    session: AsyncSession, categories: dict[str, Categories]
) -> dict[str, tuple[GoalQuestions, dict[str, GoalQuestionOptions]]]:
    questions = {}
    for question_text, question_type, category_name, sort_order, options in GOAL_QUESTIONS:
        category = categories[category_name]
        question, _ = await _get_or_create(
            session,
            GoalQuestions,
            question=question_text,
            defaults={
                "question_type": QUESTION_TYPE(question_type),
                "category_id": category.id,
                "sort_order": sort_order,
            },
        )

        question_options = {}
        for option_sort_order, label in enumerate(options):
            option, _ = await _get_or_create(
                session,
                GoalQuestionOptions,
                question_id=question.id,
                label=label,
                defaults={"sort_order": option_sort_order},
            )
            question_options[label] = option

        questions[question_text] = (question, question_options)
    return questions


async def _get_user_by_email(session: AsyncSession, email: str) -> Users:
    user = (await session.execute(select(Users).filter_by(email=email))).scalar_one_or_none()
    if user is None:
        raise ValueError(f"No user found with email {email!r}; create the user first (e.g. via seed_users or signup).")
    return user


async def seed_user_goal_answers(
    session: AsyncSession,
    questions: dict[str, tuple[GoalQuestions, dict[str, GoalQuestionOptions]]],
) -> None:
    for entry in USER_GOAL_ANSWERS:
        user = await _get_user_by_email(session, entry["user_email"])
        for answer in entry["answers"]:
            question, question_options = questions[answer["question"]]
            if "answer_text" in answer:
                await _get_or_create(
                    session,
                    UserGoalAnswers,
                    user_id=user.id,
                    question_id=question.id,
                    option_id=None,
                    defaults={"answer_text": answer["answer_text"]},
                )
            else:
                for label in answer["options"]:
                    option = question_options[label]
                    await _get_or_create(
                        session,
                        UserGoalAnswers,
                        user_id=user.id,
                        question_id=question.id,
                        option_id=option.id,
                    )


async def seed_user_conditions(session: AsyncSession) -> None:
    for entry in USER_CONDITIONS:
        user = await _get_user_by_email(session, entry["user_email"])
        await _get_or_create(
            session,
            UserConditions,
            user_id=user.id,
            condition_name=entry["condition_name"],
            defaults={"notes": entry.get("notes")},
        )


async def seed() -> None:
    async with Async_session() as session:
        async with session.begin():
            roles = await seed_roles(session)
            muscles = await seed_muscles(session)
            categories = await seed_categories(session)
            await seed_ai_catalog(session)
            users = await seed_users(session, roles)
            gyms = await seed_gyms(session, users)
            main_gym = next(iter(gyms.values()))
            equipment_catalog = await seed_equipment_catalog(session)
            gym_equipment = await seed_gym_equipment(session, main_gym, equipment_catalog)
            await seed_exercises(session, muscles, gym_equipment)
            questions = await seed_goal_questions(session, categories)
            await seed_user_goal_answers(session, questions)
            await seed_user_conditions(session)

    print("Database seeding complete.")


if __name__ == "__main__":
    asyncio.run(seed())
