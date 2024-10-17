import grpc
from concurrent import futures
import greet_pb2
import greet_pb2_grpc


# Implement the Greeter service
class GreeterServicer(greet_pb2_grpc.GreeterServicer):
    def Greet(self, request, context):
        # Generate a greeting message using the provided name
        response_message = f"Hello, {request.name}!"
        return greet_pb2.GreetResponse(message=response_message)


def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # Add the Greeter service to the server
    greet_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    # Listen on port 50051
    server.add_insecure_port("[::]:50051")
    # Start the server
    server.start()
    print("Server is running on port 50051...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
