"""Клиент уведомлений: входит в API, подключается к WebSocket и печатает уведомления.

Запуск: python notification_client/client.py <username> <password>
"""
import asyncio
import json
import sys
import urllib.parse
import urllib.request

import websockets

API_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8001/ws"


def login(username: str, password: str) -> str:
    data = urllib.parse.urlencode({"username": username, "password": password}).encode()
    with urllib.request.urlopen(urllib.request.Request(f"{API_URL}/login", data=data)) as response:
        return json.load(response)["access_token"]


async def listen(username: str, token: str) -> None:
    async with websockets.connect(f"{WS_URL}?token={token}") as websocket:
        print(f"[Клиент {username}] Подключён к {WS_URL}, ожидание уведомлений...", flush=True)
        async for message in websocket:
            notification = json.loads(message)
            print(f"[Клиент {username}] Уведомление: {notification['text']}", flush=True)


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit("Использование: python notification_client/client.py <username> <password>")
    username, password = sys.argv[1], sys.argv[2]
    token = login(username, password)
    try:
        asyncio.run(listen(username, token))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
