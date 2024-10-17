import grpc
import greet_pb2
import greet_pb2_grpc
import sys


def run(name):
    # Connect to the server
    with grpc.insecure_channel("localhost:50051") as channel:
        # Create a stub (client)
        stub = greet_pb2_grpc.GreeterStub(channel)
        # Create a GreetRequest message
        request = greet_pb2.GreetRequest(name=name)
        # Call the Greet method
        response = stub.Greet(request)
        # Print the response
        print(f"Client 1 received: {response.message}")


if __name__ == "__main__":
    name = sys.argv[1]
    run(name)
