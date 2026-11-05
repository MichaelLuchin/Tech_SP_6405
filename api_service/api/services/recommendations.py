import grpc
from fastapi import HTTPException, status

from app.models import User
from api.grpc_client import RecommenderClient
from api.schemas import RecommendedPostRead


class RecommendationService:
    def __init__(self, client: RecommenderClient) -> None:
        self.client = client

    def recommend(self, user: User, limit: int) -> list[RecommendedPostRead]:
        print(f"[API] Вызов gRPC GetRecommendations: user_id={user.id}, limit={limit}", flush=True)
        try:
            posts = self.client.get_recommendations(user.id, limit)
        except grpc.RpcError:
            raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Сервис рекомендаций недоступен")
        print(f"[API] Ответ gRPC: post_ids={[p.post_id for p in posts]}", flush=True)
        return [
            RecommendedPostRead(post_id=p.post_id, author_id=p.author_id, content=p.content, score=p.score)
            for p in posts
        ]
