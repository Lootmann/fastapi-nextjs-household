import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from api.db import Base


class Household(Base):
    __tablename__ = "households"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[int]
    registered_at: Mapped[datetime.datetime]

    # category
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship(back_populates="households")

    def __repr__(self) -> str:
        return f"<Household ({self.id}, {self.amount}, {self.registered_at})>"
