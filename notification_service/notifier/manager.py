import pickle

from websockets.asyncio.server import ServerConnection


class ConnectionManager:
    """Хранит активные WebSocket-подключения: user_id -> множество соединений."""

    def __init__(self) -> None:
        self.connections: dict[int, set[ServerConnection]] = {}

    def connect(self, user_id: int, websocket: ServerConnection) -> None:
        self.connections.setdefault(user_id, set()).add(websocket)

    def disconnect(self, user_id: int, websocket: ServerConnection) -> None:
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
                await websocket.send(pickle.dumps(message))
                delivered += 1
            except Exception:
                self.disconnect(user_id, websocket)
        return delivered
