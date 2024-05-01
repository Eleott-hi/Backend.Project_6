import database.models.models as models
from sqlmodel import SQLModel, create_engine, Session, select
from sqlalchemy.orm import load_only
from config import DB_URL
from database.fill_database import fill_database
from sqlalchemy_utils import database_exists, create_database


engine = create_engine(DB_URL, echo=True)


def create_db(engine, tables):
    if not database_exists(engine.url):
        create_database(engine.url)

    SQLModel.metadata.create_all(engine, tables=tables)


def init_db():
    global engine

    print("Initialize database models")
    create_db(
        engine,
        tables=[
            models.Address.__table__,
            models.Supplier.__table__,
            models.Product.__table__,
            models.Client.__table__,
        ],
    )

    print("Fill database models")
    fill_database(engine)

    print("Finish Initializing database models")


def get_session():
    with Session(engine) as session:
        yield session
