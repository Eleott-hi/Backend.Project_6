from typing import List
from database.models.models import Product, Supplier
from database.database import engine, load_only, select, Session
from fastapi.exceptions import HTTPException
from uuid import UUID
from repositories.Interfaces.IProductRepository import IProductRepository


class ProductRepository(IProductRepository):
    def __get_or_404(
        self,
        cls: type,
        id: UUID,
        detail: str = "Product not found",
        session: Session = None,
    ):
        item = session.get(cls, id)
        if not item:
            raise HTTPException(status_code=404, detail=detail)

        return item

    async def all(self, offset: int, limit: int) -> List[Product]:
        with Session(engine) as session:
            query = select(Product).offset(offset).limit(limit)
            res = session.exec(query).all()
            return res

    async def one(self, id: UUID) -> Product:
        with Session(engine) as session:
            product = self.__get_or_404(Product, id, session=session)

            return product

    async def one_by_image_id(self, image_id: UUID) -> Product:
        with Session(engine) as session:
            query = select(Product).where(Product.image_id == image_id)
            return session.exec(query).first()

    async def exist(self, id: UUID) -> bool:
        with Session(engine) as session:
            query = (
                select(Product, Product.id)
                .where(Product.id == id)
                .options(load_only("id"))
            )
            return bool(session.exec(query).first())

    async def create(self, product: Product) -> Product:
        with Session(engine) as session:
            if product.supplier_id:
                supplier = self.__get_or_404(
                    Supplier, product.supplier_id, "Supplier not found", session=session
                )

            session.add(product)
            session.commit()
            session.refresh(product)

            return product

    async def delete(self, id: UUID) -> str:
        with Session(engine) as session:
            product = self.__get_or_404(Product, id, session=session)
            session.delete(product)
            session.commit()

            return "Product deleted successfully"

    async def update_stock_and_price(
        self, id: UUID, price: float, stock: int
    ) -> Product:
        with Session(engine) as session:
            product = self.__get_or_404(Product, id, session=session)

            product.price = price
            product.available_stock = stock
            session.add(product)
            session.commit()
            session.refresh(product)

            return product

    async def set_image_id(self, id: UUID, image_id: UUID | None) -> None:
        with Session(engine) as session:
            product = self.__get_or_404(Product, id, session=session)
            product.image_id = image_id
            session.add(product)
            session.commit()
