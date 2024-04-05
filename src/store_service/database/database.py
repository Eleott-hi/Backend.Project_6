import database.models.models as models
from sqlmodel import SQLModel, create_engine, Session
from config import DB_URL
from database.fill_database import fill_database


engine = create_engine(DB_URL, echo=True)


def init_db():
    global engine

    print("Initialize database models")
    SQLModel.metadata.create_all(engine)

    print("Fill database models")
    fill_database(engine)

    print("Finish Initializing database models")


def get_session():
    with Session(engine) as session:
        yield session
