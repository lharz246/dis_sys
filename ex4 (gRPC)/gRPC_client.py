import grpc
import greet_pb2
import greet_pb2_grpc
import sys


def run(name, id):
    # Connect to the server
    with grpc.insecure_channel("localhost:50051") as channel:
        # Create a stub (client)
        stub = greet_pb2_grpc.GreeterStub(channel)
        # Create a GreetRequest message
        request = greet_pb2.GreetRequest(name=name)
        # Call the Greet method
        response = stub.Greet(request)
        # Print the response
        print(f"Client {id} received: {response.message}")


def chat():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = greet_pb2_grpc.GreeterStub(channel)

        # Create a generator for sending chat messages
        def request_generator():
            while True:
                message = input("Enter message: ")
                yield greet_pb2.ChatMessage(sender="Client 1", message=message)

        # Call the Chat method and get the response stream
        responses = stub.Chat(request_generator())
        for response in responses:
            print(f"Server responded: {response.message}")


if __name__ == "__main__":
    name = sys.argv[1]
    id = sys.argv[2]
    run(name, id)
    chat()
