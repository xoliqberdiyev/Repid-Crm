from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from typing import Dict, Tuple, List

import json

class ConnectionManager:
    def __init__(self):
        # Store room_id -> List of (username, WebSocket)
        self.room: Dict[str, List[Tuple[str, WebSocket]]] = {}

    async def connect(self, websocket: WebSocket, room_id: str, username: str):
        await websocket.accept()
        if room_id not in self.room:
            self.room[room_id] = []
        
        if len(self.room[room_id]) < 2:
            self.room[room_id].append((username, websocket))
        else:
            await websocket.send_text(json.dumps({"error": "Only two users can communicate"}))
            await websocket.close()

    async def disconnect(self, websocket: WebSocket, room_id: str):
        if room_id in self.room:
            self.room[room_id] = [(user, ws) for user, ws in self.room[room_id] if ws != websocket]
            if not self.room[room_id]:
                del self.room[room_id]

    async def send_message(self, sender_ws: WebSocket, message: str, room_id: str):
        if room_id in self.room:
            sender_name = None
            receiver_name = None
            receiver_ws = None

            for username, ws in self.room[room_id]:
                if ws == sender_ws:
                    sender_name = username
                else:
                    receiver_name = username
                    receiver_ws = ws

            if receiver_ws:
                json_message = json.dumps({
                    "from": sender_name,
                    "to": receiver_name,
                    "message": message
                })
                await receiver_ws.send_text(json_message)




