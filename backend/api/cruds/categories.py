from typing import List

from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import api.models.categories as category_model
from api.models import categories as category_model
from api.schemas import categories as category_schema


async def create_categories(
    db: AsyncSession, category_create: category_schema.CategoryCreate, user_id: int
) -> category_model.Category:
    category = category_model.Category(**category_create.dict())
    category.user_id = user_id

    db.add(category)
    await db.commit()
    await db.refresh(category)

    return category


async def get_categories(db: AsyncSession) -> List[category_model.Category]:
    result: Result = await (
        db.execute(
            select(
                category_model.Category.id,
                category_model.Category.name,
                category_model.Category.user_id,
            )
        )
    )
    return result.all()  # type: ignore


async def get_category(db: AsyncSession, category_id: int) -> category_model.Category | None:
    result: Result = await db.execute(select(category_model.Category).filter_by(id=category_id))
    category = result.first()
    return category[0] if category else None


async def update_category(
    db: AsyncSession,
    category_create: category_schema.CategoryCreate,
    updated: category_model.Category,
) -> category_model.Category:
    updated.name = category_create.name

    db.add(updated)
    await db.commit()
    await db.refresh(updated)
    return updated


async def delete_category(db: AssertionError, category: category_model.Category) -> None:
    await db.delete(category)
    await db.commit()
    return
