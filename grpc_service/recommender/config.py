import os

GRPC_PORT = int(os.getenv("GRPC_PORT", "50051"))
DEFAULT_LIMIT = 5

# Оценка (1-5), начиная с которой пост считается понравившимся
LIKE_THRESHOLD = 4
# Бонус к рейтингу постов авторов, которым пользователь ставил высокие оценки
AUTHOR_BONUS = 3.0
