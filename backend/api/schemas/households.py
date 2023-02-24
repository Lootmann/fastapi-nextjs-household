from datetime import datetime

from pydantic import BaseModel, Field


class HouseholdBase(BaseModel):
    amount: int
    category_id: int
    registered_at: datetime

    class Config:
        orm_mode = True


class HouseholdCreate(HouseholdBase):
    pass


class HouseholdCreateResponse(HouseholdCreate):
    id: int
    user_id: int


class HouseholdUpdate(BaseModel):
    amount: int = Field(0)
    category_id: int = Field(0)

    class Config:
        orm_mode = True


class Household(HouseholdBase):
    id: int
    user_id: int
