from concurrent import futures

import grpc

import recommendations_pb2
import recommendations_pb2_grpc
from app.database import SessionLocal
from app.repositories import PostRepository, RatingRepository
from recommender.config import DEFAULT_LIMIT, GRPC_PORT
from recommender.service import RecommendationService


class RecommenderServicer(recommendations_pb2_grpc.RecommenderServicer):
    def GetRecommendations(self, request, context):
        limit = request.limit or DEFAULT_LIMIT
        print(f"[gRPC] GetRecommendations: user_id={request.user_id}, limit={limit}", flush=True)

        with SessionLocal() as db:
            service = RecommendationService(PostRepository(db), RatingRepository(db))
            items = service.recommend(request.user_id, limit)
            posts = [
                recommendations_pb2.RecommendedPost(
                    post_id=post.id, author_id=post.author_id, content=post.content, score=score
                )
                for post, score in items
            ]

        print(f"[gRPC] Ответ: post_ids={[p.post_id for p in posts]}", flush=True)
        return recommendations_pb2.RecommendationResponse(posts=posts)


def serve() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    recommendations_pb2_grpc.add_RecommenderServicer_to_server(RecommenderServicer(), server)
    server.add_insecure_port(f"[::]:{GRPC_PORT}")
    server.start()
    print(f"[gRPC] Сервис рекомендаций запущен на порту {GRPC_PORT}", flush=True)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
