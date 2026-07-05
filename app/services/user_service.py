from app.repositories import user_repository


def get_all_users():
    return user_repository.get_all_users()