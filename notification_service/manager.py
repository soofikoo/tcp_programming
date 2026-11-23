from collections import defaultdict
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.connections: dict[int, set[WebSocket]] = defaultdict(set)

    async def connect(self, user_id: int, ws: WebSocket):
        await ws.accept()
        self.connections[user_id].add(ws)
        print(f"[NS] user {user_id} онлайн, соединений: {len(self.connections[user_id])}")

    def disconnect(self, user_id: int, ws: WebSocket):
        self.connections[user_id].discard(ws)
        if not self.connections[user_id]:
            del self.connections[user_id]
        print(f"[NS] user {user_id} отключился")

    async def send_to_user(self, user_id: int, data: dict) -> bool:
        sockets = list(self.connections.get(user_id, ()))
        for ws in sockets:
            try:
                await ws.send_json(data)
            except Exception:
                self.disconnect(user_id, ws)
        return bool(sockets)

manager = ConnectionManager()