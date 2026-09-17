from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from jose import jwt, JWTError
from app.config import settings
from app.websocket.manager import manager

router = APIRouter()

@router.websocket("/ws/sensors")
async def sensor_ws(websocket: WebSocket, token: str = Query(...)):
    try:
        jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError:
        await websocket.close(code=1008)
        return

    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)