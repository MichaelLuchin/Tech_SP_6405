from fastapi import WebSocket


class ConnectionManager:
    """Хранит активные WebSocket-подключения: user_id -> множество соединений."""

    def __init__(self) -> None:
        self.connections: dict[int, set[WebSocket]] = {}

    async def connect(self, user_id: int, websocket: WebSocket) -> None:
        await websocket.accept()
        self.connections.setdefault(user_id, set()).add(websocket)

    def disconnect(self, user_id: int, websocket: WebSocket) -> None:
        sockets = self.connections.get(user_id)
        if sockets is None:
            return
        sockets.discard(websocket)
        if not sockets:
            del self.connections[user_id]

    async def send_to_user(self, user_id: int, message: dict) -> int:
        """Отправляет сообщение всем подключениям пользователя. Возвращает число доставок."""
        delivered = 0
        for websocket in list(self.connections.get(user_id, ())):
            try:
                await websocket.send_json(message)
                delivered += 1
            except Exception:
                self.disconnect(user_id, websocket)
        return delivered
