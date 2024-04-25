from opyoid import Module
from routers.ClientRouter import ClientRouter
from routers.ProductRouter import ProductRouter
from routers.SupplierRouter import SupplierRouter
from image_service.routers.ImageRouter import ImageRouter


# class RoutersInjector(Module):
#     def configure(self):
#         self.bind(ClientRouter)
#         self.bind(ProductRouter)
#         self.bind(SupplierRouter)
#         self.bind(ImageRouter)
