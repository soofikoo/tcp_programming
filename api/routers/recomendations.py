import grpc
from fastapi import APIRouter, Depends, HTTPException, status

from api.deps import get_current_user, get_db
from api.grpc_client import get_recommendation_stub
from api.schemas.recomendation import RecommendationOut
from models import User
from services.tracks_service import get_tracks_by_ids
from protos import recommendation_pb2 as pb2

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

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
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "GRPC Service Unavailable")

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