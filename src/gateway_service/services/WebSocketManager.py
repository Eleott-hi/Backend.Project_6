from typing import List
from fastapi import WebSocket
from singleton_decorator import singleton

@singleton
class WebSocketManager():
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str):
        for connection in self.active_connections:
            await connection.send_json(message)

    async def send_message_callback(self, message: str):
        await self.send_message(message)
