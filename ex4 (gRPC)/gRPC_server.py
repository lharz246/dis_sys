import json

import grpc
from concurrent import futures
import server_pb2
import server_pb2_grpc
from threading import Lock

# Dictionary to keep track of all active clients: {client_id: response_stream}
connected_clients = {}
clients_lock = Lock()


class ServerServicer(server_pb2_grpc.ServerServicer):
    def Greet(self, request, context):
        print(f"Greet request from {request.name}")
        response_message = f"Hello, {request.name}!"
        with clients_lock:
            connected_clients[request.name] = request.address
        return server_pb2.GreetResponse(message=response_message)

    def Client(self, request, context):
        print(f"Client request from {request.name}")
        print(connected_clients)
        try:
            with clients_lock:
                adress_names = json.dumps(connected_clients)
                return server_pb2.ClientResponse(address_name=adress_names)
        except Exception as e:
            return server_pb2.ClientResponse(address_name="Unknown Client!")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server_pb2_grpc.add_ServerServicer_to_server(ServerServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server is running on port 50051...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
