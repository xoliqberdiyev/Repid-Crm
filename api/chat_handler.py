from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from websocket.manager import ConnectionManager 

from api.login_handler import get_current_user_from_token

chat_handler = APIRouter()

manager = ConnectionManager()


# @chat_handler.websocket('/ws/{room_id}')
# async def websocket_endpoint(
#     websocket: WebSocket, 
#     room_id: str, 
#     username: str = Depends(get_current_user_from_token)
# ):
#     await manager.connect(websocket, room_id, username)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await manager.send_message(websocket, data, room_id)
#     except WebSocketDisconnect:
#         await manager.disconnect(websocket, room_id)
#         await manager.send_message(websocket, "A user just left the chat", room_id)