import database.models.models as models
import database.models.image as image
from sqlmodel import SQLModel, create_engine, Session
from config import DB_URL, IMAGE_DB_1, IMAGE_DB_2, IMAGE_DB_3, IMAGE_DB_4
from database.fill_database import fill_database


engine = create_engine(DB_URL, echo=True)
img_engine_1 = create_engine(IMAGE_DB_1, echo=True)
img_engine_2 = create_engine(IMAGE_DB_2, echo=True)
img_engine_3 = create_engine(IMAGE_DB_3, echo=True)
img_engine_4 = create_engine(IMAGE_DB_4, echo=True)


def init_db():
    global engine

    print("Initialize database models")
    SQLModel.metadata.create_all(
        engine,
        tables=[
            models.Address.__table__,
            models.Supplier.__table__,
            models.Product.__table__,
            models.Client.__table__,
        ],
    )

    SQLModel.metadata.create_all(img_engine_1, tables=[image.Image.__table__])
    SQLModel.metadata.create_all(img_engine_2, tables=[image.Image.__table__])
    SQLModel.metadata.create_all(img_engine_3, tables=[image.Image.__table__])
    SQLModel.metadata.create_all(img_engine_4, tables=[image.Image.__table__])

    print("Fill database models")
    fill_database(engine)

    print("Finish Initializing database models")


def get_session():
    with Session(engine) as session:
        yield session
