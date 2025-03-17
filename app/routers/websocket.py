import logging

from fastapi import APIRouter, WebSocket

router = APIRouter(
    prefix="/ws",
    responses={404: {"description": "Not found"}},
)

@router.websocket('/echo')
async def accept(websocket: WebSocket):
    await websocket.accept()
    print("Yeah!")
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"echo: {data}")

