from fastapi import APIRouter, Query

from api.dependencies import CurrentUser, RecommendationServiceDep
from api.schemas import RecommendedPostRead

router = APIRouter(tags=["recommendations"])


@router.get("/recommendations", response_model=list[RecommendedPostRead])
def get_recommendations(
    user: CurrentUser,
    service: RecommendationServiceDep,
    limit: int = Query(5, ge=1, le=20),
):
    return service.recommend(user, limit)
