import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, status

from notification_service.consumer import consume
from notification_service.manager import manager
from notification_service.security import user_id_from_token

async def on_track_created(event):
    notification = {
        "type": "new_track",
        "text": f"{event.artist_name} выпустил(а) новый трек «{event.title}»",
        "track_id": event.track_id,
        "artist_id": event.artist_id,
        "created_at": event.created_at.isoformat(),
    }
    delivered = 0
    for uid in event.subscriber_ids:
        if await manager.send_to_user(uid, notification):
            delivered += 1
    print(f"[NS] → WebSocket: доставлено {delivered} из {len(event.subscriber_ids)} (остальные офлайн)")

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(consume(on_track_created))
    yield
    task.cancel()

app = FastAPI(title="Notification Service", lifespan=lifespan)

@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket, token: str):
    user_id = user_id_from_token(token)
    if user_id is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    await manager.connect(user_id, websocket)
    try:
        while True:
            await websocket.receive_text()     # держим соединение; клиент может слать ping
    except WebSocketDisconnect:
        manager.disconnect(user_id, websocket)
