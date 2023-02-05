from typing import List
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

import api.models.categories as category_model
import api.schemas.categories as category_schema


async def create_categories(
    db: AsyncSession, category_create: category_schema.CategoryCreate
) -> category_model.Category:
    category = category_model.Category(**category_create.dict())

    db.add(category)
    await db.commit()
    await db.refresh(category)

    return category


async def get_categories(db: AsyncSession) -> List[category_model.Category] | None:
    result: Result = await (
        db.execute(
            select(
                category_model.Category.id,
                category_model.Category.name,
            )
        )
    )
    return result.all()
