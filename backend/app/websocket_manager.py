from fastapi import WebSocket
import json

class ConnectionManager:
    """
    Manages active WebSocket connections.
    """
    def __init__(self):
        # A dictionary to store active connections, mapping a client_id to a WebSocket object.
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        """Accepts and stores a new WebSocket connection."""
        await websocket.accept()
        self.active_connections[client_id] = websocket
        print(f"New connection: {client_id} connected.")

    def disconnect(self, client_id: str):
        """Removes a WebSocket connection."""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            print(f"Connection closed: {client_id} disconnected.")

    async def send_personal_message(self, message: dict, client_id: str):
        """Sends a JSON message to a specific client."""
        if client_id in self.active_connections:
            websocket = self.active_connections[client_id]
            await websocket.send_json(message)
