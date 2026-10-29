import os, grpc
from protos import recommendation_pb2_grpc as pb2_grpc

_channel = grpc.insecure_channel(os.getenv("RECOMMENDATION_ADDR", "localhost:50051"))
_stub = pb2_grpc.RecommendationStub(_channel)

def get_recommendation_stub():
    return _stub