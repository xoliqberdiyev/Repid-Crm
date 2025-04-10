from fastapi import WebSocket, WebSocketDisconnect

from typing import Dict, Tuple, List

import os
import base64
import json

MEDIA_PATH = "media/messages"

class ConnectionManager:
    def __init__(self):
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

    async def send_message(self, sender_ws: WebSocket, data: dict, room_id: str):
        if room_id not in self.room:
            return

        sender_name = None
        receiver_ws = None
        receiver_name = None

        for username, ws in self.room[room_id]:
            if ws == sender_ws:
                sender_name = username
            else:
                receiver_ws = ws
                receiver_name = username

        if not receiver_ws:
            return

        msg_type = data.get("type", "text")

        if msg_type == "text":
            content = data.get("message", "")
            response = {
                "type": "text",
                "from": sender_name,
                "to": receiver_name,
                "message": content
            }
            await receiver_ws.send_text(json.dumps(response))

        if msg_type == "file":
            filename = data.get("filename")
            filetype = data.get("filetype")
            content = data.get("content")  # base64 string

            if not all([filename, filetype, content]):
                await sender_ws.send_text(json.dumps({"error": "Missing file data"}))
                return

            # 1. Decode and save file
            os.makedirs(MEDIA_PATH, exist_ok=True)
            file_path = os.path.join(MEDIA_PATH, filename)

            with open(file_path, "wb") as f:
                f.write(base64.b64decode(content))

            # 2. Return file URL to receiver
            file_url = f"/media/messages/{filename}"
            await receiver_ws.send_text(json.dumps({
                "type": "file",
                "from": sender_name,
                "to": receiver_name,
                "filename": filename,
                "filetype": filetype,
                "url": file_url
            }))



