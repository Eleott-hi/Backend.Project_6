from database.models.image import Image
from database.models.models import Product
from sqlmodel import Session
from database.database import (
    engine,
    img_engine_1,
    img_engine_2,
    img_engine_3,
    img_engine_4,
)
from fastapi.exceptions import HTTPException
from uuid import UUID, uuid4
from repositories.Interfaces.IImageRepository import IImageRepository


class ImageRepository(IImageRepository):

    async def one(self, id: UUID) -> bytes:
        img_engine = self.get_image_engine(id)

        with Session(img_engine) as session:
            image = self.__get_or_404(Image, id, session=session)
            return image.image

    async def one_by_product_id(self, id: UUID) -> bytes:
        with Session(engine) as session:
            product = self.__get_or_404(
                Product, id, "Product not found", session=session
            )

            if product.image_id is None:
                raise HTTPException(status_code=404, detail="Product has no image")

        img_engine = self.get_image_engine(product.image_id)
        with Session(img_engine) as session:
            image = self.__get_or_404(Image, product.image_id, session=session)

            return image.image

    async def create(self, image: Image, product_id: UUID) -> Image:
        img_id = uuid4()
        image.id = img_id

        img_engine = self.get_image_engine(img_id)

        with Session(img_engine) as session:
            session.add(image)
            session.commit()

        with Session(engine) as session:
            product = self.__get_or_404(
                Product, product_id, "Product not found", session=session
            )

            product.image_id = img_id
            session.add(product)
            session.commit()

            return image

    async def update(self, id: UUID, image_info: bytes) -> Image:
        img_engine = self.get_image_engine(id)

        with Session(img_engine) as session:
            image = self.__get_or_404(Image, id, session=session)
            image.image = image_info

            session.add(image)
            session.commit()

            return "Image updated successfully"

    async def delete(self, id: UUID) -> str:
        img_engine = self.get_image_engine(id)

        with Session(img_engine) as session:
            image = self.__get_or_404(Image, id, session=session)
            session.delete(image)
            session.commit()

            return "Image deleted successfully"

    def __get_or_404(
        self,
        cls: type,
        id: UUID,
        detail: str = "Image not found",
        session: Session = None,
    ):
        item = session.get(cls, id)

        if not item:
            raise HTTPException(status_code=404, detail=detail)

        return item

    def get_image_engine(self, id: UUID) -> Session:
        letter = str(id)[0]

        if letter in "0123":
            return img_engine_1
        elif letter in "4567":
            return img_engine_2
        elif letter in "89ab":
            return img_engine_3
        elif letter in "cdef":
            return img_engine_4
        else:
            raise HTTPException(status_code=404, detail="Image not found")
