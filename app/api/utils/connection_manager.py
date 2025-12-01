from typing import List
from fastapi.websockets import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []


    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    @staticmethod
    async def send_personal_message( message: str, websocket: WebSocket):
        await websocket.send_text(message)


    async def broadcast(self, message: str):
        for connection in self.connections:
            try:
                await connection.send_json(message)
            except WebSocketDisconnect:
                self.disconnect(connection)

