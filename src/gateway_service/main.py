from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from services.SSEManager import SSEManager
from services.KafkaManager import KafkaManager
from services.WebSocketManager import WebSocketManager
from services.utils import update_db_callback

from routers.WebSocketRouter import router as ws_router
from routers.SSERouter import router as sse_router

sse_manager = SSEManager()
ws_manager = WebSocketManager()
consumer = KafkaManager()


async def lifespan(app: FastAPI):
    consumer.add_callback(update_db_callback)
    consumer.add_callback(ws_manager.send_message_callback)
    consumer.add_callback(sse_manager.update_data)
    asyncio.create_task(consumer.consume_async())

    yield


app = FastAPI(
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ws_router)
app.include_router(sse_router)


# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
