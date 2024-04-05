from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from services.SSEManager import SSEManager


router = APIRouter(
    prefix="/sse",
    tags=["WebSocket"],
)


@router.get("/")
async def sse(sse_manager=Depends(SSEManager)):
    return StreamingResponse(sse_manager.streaming(), media_type="text/event-stream")
