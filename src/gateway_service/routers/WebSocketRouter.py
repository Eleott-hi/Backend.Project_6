from fastapi import APIRouter, WebSocket, Depends
from services.WebSocketManager import WebSocketManager


router = APIRouter(
    prefix="/ws",
    tags=["WebSocket"],
)


@router.websocket("/")
async def websocket_endpoint(
    websocket: WebSocket,
    ws_manager: WebSocketManager = Depends(WebSocketManager),
):
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await ws_manager.send_message(f"Message text was: {data}")
            print(data, flush=True)

    except Exception as e:
        ws_manager.disconnect(websocket)
