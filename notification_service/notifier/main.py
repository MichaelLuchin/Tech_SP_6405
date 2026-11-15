from contextlib import asynccontextmanager

import jwt
from fastapi import FastAPI, Query, WebSocket, WebSocketDisconnect, status

from notifier.consumer import start_consumer
from notifier.manager import ConnectionManager
from notifier.security import decode_access_token

manager = ConnectionManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    connection = await start_consumer(manager)
    print("[Notifier] Подключено к RabbitMQ, ожидание событий", flush=True)
    yield
    await connection.close()


app = FastAPI(title="Notification Service", version="1.0", lifespan=lifespan)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):
    try:
        user_id = decode_access_token(token)
    except jwt.InvalidTokenError:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(user_id, websocket)
    print(f"[Notifier] Клиент подключился: user_id={user_id}", flush=True)
    try:
        while True:
            await websocket.receive_text()  # клиент ничего не шлёт; цикл нужен, чтобы заметить отключение
    except WebSocketDisconnect:
        manager.disconnect(user_id, websocket)
        print(f"[Notifier] Клиент отключился: user_id={user_id}", flush=True)
