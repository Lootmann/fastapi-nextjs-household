from sqlalchemy import create_engine

from api.models.categories import Base as category_base

DB_URL = "sqlite:///db.sqlite3"
engine = create_engine(DB_URL, echo=True)


def reset_database():
    category_base.metadata.drop_all(bind=engine)
    category_base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database()
