import pickle

import pika

from api.config import NOTIFICATIONS_QUEUE, RABBITMQ_URL


class EventPublisher:
    """Публикует события в очередь RabbitMQ."""

    def __init__(self, url: str = RABBITMQ_URL, queue: str = NOTIFICATIONS_QUEUE) -> None:
        self.url = url
        self.queue = queue

    def publish(self, event: dict) -> None:
        # BlockingConnection не потокобезопасен, а обработчики FastAPI работают в пуле потоков,
        # поэтому на каждое событие открывается отдельное короткое соединение.
        try:
            connection = pika.BlockingConnection(pika.URLParameters(self.url))
            try:
                channel = connection.channel()
                channel.queue_declare(queue=self.queue, durable=True)
                channel.basic_publish(
                    exchange="",
                    routing_key=self.queue,
                    body=pickle.dumps(event),
                    properties=pika.BasicProperties(
                        content_type="application/json",
                        delivery_mode=pika.DeliveryMode.Persistent,
                    ),
                )
            finally:
                connection.close()
            print(f"[API] Событие отправлено в RabbitMQ: {event}", flush=True)
        except (pika.exceptions.AMQPError, OSError):
            # недоступность брокера не должна ломать основной запрос
            print(f"[API] RabbitMQ недоступен, событие не отправлено: {event}", flush=True)
