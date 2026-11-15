import os

from dotenv import load_dotenv

load_dotenv()

# RabbitMQ
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
NOTIFICATIONS_QUEUE = "notifications"

# JWT (те же значения, что в API Service)
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-change-me")
ALGORITHM = "HS256"
