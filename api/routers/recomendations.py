import grpc
from fastapi import APIRouter, Depends, HTTPException, status

from api.deps import get_current_user, get_db
from api.grpc_client import get_recommendation_stub
from api.schemas.recomendation import RecommendationOut
from models import User
from services.tracks_service import get_tracks_by_ids
from protos import recommendation_pb2 as pb2

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

GRPC_TO_HTTP = {
    grpc.StatusCode.UNAVAILABLE: (status.HTTP_503_SERVICE_UNAVAILABLE, "Recommendation service is unavailable"),
    grpc.StatusCode.DEADLINE_EXCEEDED: (status.HTTP_504_GATEWAY_TIMEOUT, "Recommendation service timed out"),
    grpc.StatusCode.INVALID_ARGUMENT: (status.HTTP_400_BAD_REQUEST, "Invalid recommendation request"),
    grpc.StatusCode.NOT_FOUND: (status.HTTP_404_NOT_FOUND, "User not found"),
}

@router.get("", response_model=list[RecommendationOut])
def recommendations(limit: int = 10,
                    user: User = Depends(get_current_user),
                    stub=Depends(get_recommendation_stub),
                    db=Depends(get_db)):
    try:
        reply = stub.GetRecommendations(
            pb2.RecommendationRequest(user_id=user.id, limit=limit), timeout=2
        )
    except grpc.RpcError as e:
        http_status, detail = GRPC_TO_HTTP.get(
            e.code(),
            (status.HTTP_503_SERVICE_UNAVAILABLE, "Recommendation service error"),
        )
        raise HTTPException(status_code=http_status, detail=detail)

    tracks = get_tracks_by_ids(db, [t.track_id for t in reply.tracks])

    result = []
    for t in reply.tracks:
        info = tracks.get(t.track_id)
        if info is None:
            continue
        title, artist_name = info
        result.append(RecommendationOut(
            track_id=t.track_id,
            title=title,
            artist_name=artist_name,
            score=t.score,
            reason=t.reason,
        ))
    return result