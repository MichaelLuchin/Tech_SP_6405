import asyncio
from urllib.parse import parse_qs, urlparse

import jwt
from websockets.asyncio.server import serve

from notifier.consumer import start_consumer
from notifier.manager import ConnectionManager
from notifier.security import decode_access_token

manager = ConnectionManager()


async def handler(websocket):
    # токен берём из адреса вручную: ws://localhost:8001/ws?token=...
    query = urlparse(websocket.request.path).query
    token = parse_qs(query).get("token", [""])[0]
    try:
        user_id = decode_access_token(token)
    except jwt.InvalidTokenError:
        await websocket.close(code=1008, reason="Invalid token")
        return

    manager.connect(user_id, websocket)
    print(f"[Notifier] Клиент подключился: user_id={user_id}", flush=True)
    try:
        await websocket.wait_closed()  # ждём, пока клиент отключится
    finally:
        manager.disconnect(user_id, websocket)
        print(f"[Notifier] Клиент отключился: user_id={user_id}", flush=True)


async def main():
    connection = await start_consumer(manager)
    print("[Notifier] Подключено к RabbitMQ, ожидание событий", flush=True)
    async with serve(handler, "0.0.0.0", 8001):
        try:
            await asyncio.Future()  # работать бесконечно
        finally:
            await connection.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass