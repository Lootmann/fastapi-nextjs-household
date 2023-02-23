from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    # ... means Required Field
    name: str = Field(..., example="category name")

    class Config:
        orm_mode = True


class CategoryCreate(CategoryBase):
    pass


class CategoryCreateResponse(CategoryBase):
    id: int


class Category(CategoryBase):
    id: int
    user_id: int
