import pickle

import aio_pika

from notifier.config import NOTIFICATIONS_QUEUE, RABBITMQ_URL
from notifier.manager import ConnectionManager


def build_notification(event: dict) -> dict | None:
    """Формирует уведомление для пользователя по событию из очереди."""
    kind = event.get("event")
    if kind == "post_created":
        text = f"{event['author_name']} опубликовал(а) новый пост #{event['post_id']}"
    elif kind == "post_rated":
        text = f"{event['user_name']} оценил(а) ваш пост #{event['post_id']} на {event['score']}"
    else:
        return None
    return {"type": kind, "text": text}


async def start_consumer(manager: ConnectionManager) -> aio_pika.abc.AbstractRobustConnection:
    """Подключается к RabbitMQ и подписывается на очередь уведомлений."""
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue(NOTIFICATIONS_QUEUE, durable=True)

    async def on_message(message: aio_pika.abc.AbstractIncomingMessage) -> None:
        # подтверждение (ack) отправляется после успешной обработки
        async with message.process():
            event = pickle.loads(message.body)
            print(f"[Notifier] Событие из RabbitMQ: {event}", flush=True)

            notification = build_notification(event)
            if notification is None:
                return
            for user_id in event.get("recipient_ids", []):
                delivered = await manager.send_to_user(user_id, notification)
                print(f"[Notifier] Уведомление для user_id={user_id}: доставлено клиентам: {delivered}", flush=True)

    await queue.consume(on_message)
    return connection
