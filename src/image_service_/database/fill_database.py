
from database.models.models import  Product
from sqlmodel import Session, select


def get_image(i: int):
    jpeg_path = f"static/Product_{i}.jpeg"
    with open(jpeg_path, "rb") as f:
        return Image(image=f.read())


products = [
    Product(
        name="Product 1",
        category="Category 1",
        price=10,
        available_stock=100,
        # image=get_image(1),
    ),
    Product(
        name="Product 2",
        category="Category 2",
        price=20,
        available_stock=200,
        # image=get_image(2),
    ),
    Product(
        name="Product 3",
        category="Category 3",
        price=30,
        available_stock=300,
        # image=get_image(3),
    ),
]


def fill_products(engine):
    with Session(engine) as session:
        for i, product in enumerate(products):
            q = select(Product).where(Product.name == product.name)

            user = session.execute(q).first()

            if not user:
                session.add(product)
                session.commit()
                session.refresh(product)


def fill_database(engine):
    fill_products(engine)
