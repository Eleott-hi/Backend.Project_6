import database.database as database
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from DependencyInjection.InjectionModule import injector
from routers.ClientRouter import ClientRouter
from routers.ProductRouter import ProductRouter
from routers.SupplierRouter import SupplierRouter
from routers.ImageRouter import ImageRouter

from contextlib import asynccontextmanager
from routers.AuthRouter import AuthRouter
from starlette.middleware.base import BaseHTTPMiddleware
from services.JWTBearer import middleware_get_token_from_cookies


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_db()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="My cool api",
    description="Some description",
    version="1.0.0",
    docs_url="/",
    openapi_url="/openapi.json",
    root_path="/api/v1",
)

app.add_middleware(
    BaseHTTPMiddleware,
    dispatch=middleware_get_token_from_cookies,
)

app.include_router(injector.inject(ClientRouter).router)
app.include_router(injector.inject(ProductRouter).router)
app.include_router(injector.inject(SupplierRouter).router)
app.include_router(injector.inject(ImageRouter).router)
app.include_router(AuthRouter().router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
