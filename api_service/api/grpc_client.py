import grpc

import recommendations_pb2
import recommendations_pb2_grpc
from api.config import GRPC_RECOMMENDER_ADDRESS


class RecommenderClient:
    """gRPC-клиент сервиса рекомендаций."""

    def __init__(self, address: str = GRPC_RECOMMENDER_ADDRESS) -> None:
        self.channel = grpc.insecure_channel(address)
        self.stub = recommendations_pb2_grpc.RecommenderStub(self.channel)

    def get_recommendations(self, user_id: int, limit: int):
        request = recommendations_pb2.RecommendationRequest(user_id=user_id, limit=limit)
        return self.stub.GetRecommendations(request, timeout=5).posts
