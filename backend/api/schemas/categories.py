from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    # ... means Required Field
    name: str = Field(..., example="category name")


class CategoryCreate(CategoryBase):
    pass


class CategoryCreateResponse(CategoryCreate):
    id: int

    class Config:
        orm_mode = True


class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True
