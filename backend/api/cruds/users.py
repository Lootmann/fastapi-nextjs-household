from typing import List

from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.models import users as user_model
from api.schemas import users as user_schema


async def create_user(
    db: AsyncSession, user_create: user_schema.UserCreateResponse
) -> user_model.User:
    user = user_model.Category(**user_create.dict())

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def get_all_users(db: AsyncSession) -> List[user_model.User]:
    pass


async def get_user(user_id: int, db: AsyncSession) -> user_model.User:
    pass


async def find_by_name(username: str, db: AsyncSession) -> user_model.User:
    pass


async def update_user(username: str, db: AsyncSession) -> user_model.User:
    pass


async def delete_user(username: str, db: AsyncSession) -> user_model.User:
    pass
