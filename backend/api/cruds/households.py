from datetime import datetime
from typing import List

from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.models import households as household_model
from api.schemas import households as household_schema


async def get_households(db: AsyncSession) -> List[household_model.Household]:
    result: Result = await (
        db.execute(
            select(
                household_model.Household.id,
                household_model.Household.amount,
                household_model.Household.registered_at,
                household_model.Household.category_id,
                household_model.Household.user_id,
            )
        )
    )
    return result.all()  # type: ignore


async def create_households(
    db: AsyncSession,
    household_create: household_schema.HouseholdCreate,
    user_id: int,
) -> household_model.Household:
    household = household_model.Household()

    household.user_id = user_id
    household.amount = household_create.amount
    household.registered_at = household_create.registered_at
    household.category_id = household_create.category_id

    db.add(household)
    await db.commit()
    await db.refresh(household)
    return household


async def find_by_id(db: AsyncSession, household_id: int) -> household_model.Household | None:
    result: Result = await db.execute(select(household_model.Household).filter_by(id=household_id))
    household = result.first()
    return household[0] if household else None


async def find_by_category(db: AsyncSession, category_id: int) -> List[household_model.Household]:
    results: Result = await db.execute(
        select(
            household_model.Household.id,
            household_model.Household.amount,
            household_model.Household.registered_at,
            household_model.Household.category_id,
            household_model.Household.user_id,
        ).filter_by(category_id=category_id)
    )
    return results.all()


async def update_household(
    db: AsyncSession,
    household: household_model.Household,
    updated_body: household_schema.HouseholdUpdate,
) -> household_model.Household:
    if updated_body.amount != 0:
        household.amount = updated_body.amount

    if updated_body.category_id != 0:
        household.category_id = updated_body.category_id

    # automatically updated
    household.registered_at = datetime.now()

    db.add(household)
    await db.commit()
    await db.refresh(household)

    return household
