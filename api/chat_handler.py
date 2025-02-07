from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends,  Query, HTTPException
from websocket.manager import ConnectionManager 
from utils.settings import SECRET_KEY, ALGORITHM
from jose import jwt, JWTError

from typing import Optional
from api.login_handler import get_current_user_from_token

chat_handler = APIRouter()

manager = ConnectionManager()

async def get_current_user_from_token(
    websocket: WebSocket, token: Optional[str] = Query(None)
):
    """
    Extracts the token from the WebSocket URL query parameter,
    decodes it, and returns the user.
    """
    if not token:
        raise HTTPException(status_code=HTTPException, detail="Token is required")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")  # Get the user from the token
        if username is None:
            raise HTTPException(status_code=HTTPException, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=HTTPException, detail="Invalid token")
    

@chat_handler.websocket('/ws/{room_id}')
async def websocket_endpoint(
    websocket: WebSocket, 
    room_id: str, 
    username: str = Depends(get_current_user_from_token)
):
    await manager.connect(websocket, room_id, username)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_message(websocket, data, room_id)
    except WebSocketDisconnect:
        await manager.disconnect(websocket, room_id)
        await manager.send_message(websocket, "A user just left the chat", room_id)