from api.models.user import User
from api.schemas.user import User as UserSchema


def get_user_schemas(users: list[User]) -> list[UserSchema]:
    return [UserSchema(id=user.id, name=user.name) for user in users]  # type: ignore


def get_user_schema(user: User) -> UserSchema:
    return UserSchema(id=user.id, name=user.name)  # type: ignore
