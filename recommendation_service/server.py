from concurrent import futures
import grpc

from database import Session
from models import User
from protos import recommendation_pb2 as pb2, recommendation_pb2_grpc as pb2_grpc
from recommendation_service.algorithm import recommend


class RecommendationServicer(pb2_grpc.RecommendationServicer):
    def GetRecommendations(self, request, context):
        print(f"[gRPC] GetRecommendations(user_id={request.user_id}, limit={request.limit})")
        limit: int = 10
        if request.limit != 0:
            limit = request.limit
        if limit < 0:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "limit must be >= 0")
        with Session() as db:
            if db.get(User, request.user_id) is None:
                context.abort(grpc.StatusCode.NOT_FOUND, "User not found")

            items, cold_start = recommend(db, request.user_id, limit)

        tracks = []
        for tid, score, reason in items:
            tracks.append(pb2.RecommendedTrack(track_id=tid, score=score, reason=reason))
            
        return pb2.RecommendationResponse(tracks=tracks, cold_start=cold_start)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_RecommendationServicer_to_server(RecommendationServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Recommendation Service запущен на :50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()