from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.db import Base
from api.models.households import Household


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    households: Mapped[List["Household"]] = relationship("Household", back_populates="category")

    def __repr__(self) -> str:
        return f"<Category ({self.id}, {self.name})>"
