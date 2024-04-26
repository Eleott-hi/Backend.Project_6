import database.database as database
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

# from DependencyInjection.InjectionModule import injector
# from routers.ClientRouter import ClientRouter
# from routers.ProductRouter import ProductRouter
# from routers.SupplierRouter import SupplierRouter
from routers.ImageRouter import router as image_router

from contextlib import asynccontextmanager
# from routers.AuthRouter import AuthRouter
# from starlette.middleware.base import BaseHTTPMiddleware
# from services.JWTBearer import middleware_get_token_from_cookies


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.init_db()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Image service",
    description="Image storage server in sharding databases",
    version="1.0.0",
    root_path="/api/v1",
)

app.include_router(image_router)

# app.add_middleware(
#     BaseHTTPMiddleware,
#     dispatch=middleware_get_token_from_cookies,
# )



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
