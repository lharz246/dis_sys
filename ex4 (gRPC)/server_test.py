import grpc
from concurrent import futures
import greet_pb2
import greet_pb2_grpc
from threading import Lock

# Dictionary to keep track of all active clients: {client_id: response_stream}
connected_clients = {}
clients_lock = Lock()


class GreeterServicer(greet_pb2_grpc.GreeterServicer):
    def Greet(self, request, context):
        response_message = f"Hello, {request.name}!"
        return greet_pb2.GreetResponse(message=response_message)

    def Chat(self, request_iterator, context):
        # Add the new client to the list of connected clients
        with clients_lock:
            connected_clients.append(context)

        try:
            # Process incoming messages from the client
            for chat_message in request_iterator:
                print(
                    f"Received message from {chat_message.sender}: {chat_message.message}"
                )

                # Broadcast the message to all connected clients
                with clients_lock:
                    for client_context in connected_clients:
                        if (
                            client_context != context
                        ):  # Skip sending the message back to the sender
                            try:
                                client_context.send_message(
                                    chat_pb2.ChatMessage(
                                        sender=chat_message.sender,
                                        message=chat_message.message,
                                        timestamp=chat_message.timestamp,
                                    )
                                )
                            except Exception as e:
                                print(f"Could not send message to client: {e}")
        except Exception as e:
            print(f"Client disconnected: {e}")
        finally:
            # Remove the client from the list when disconnected
            with clients_lock:
                connected_clients.remove(context)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    greet_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server is running on port 50051...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
