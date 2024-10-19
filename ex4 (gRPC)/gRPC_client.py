import json
import struct
import sys

import grpc
from concurrent import futures
import chat_pb2
import chat_pb2_grpc
import server_pb2
import server_pb2_grpc
import threading
import time


class ChatServicer(chat_pb2_grpc.ChatServicer):

    def ReceiveMessages(self, request, context):
        print(f"{request.sender} ({request.timestamp}): {request.message}")
        return chat_pb2.ChatMessageResponse(message=1)

    def SendMessage(self, request, context, message, name):
        timestemp = time.time()
        return chat_pb2.ChatMessage(message=message, sender=name, timestemp=timestemp)


def main(name, port):
    address = f"localhost:{port}"
    chat_server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    chat_pb2_grpc.add_ChatServicer_to_server(ChatServicer(), chat_server)
    chat_server.add_insecure_port(f"[::]:{port}")
    chat_server.start()
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = server_pb2_grpc.ServerStub(channel)
        request = server_pb2.GreetRequest(name=name, address=address)
        response = stub.Greet(request)
        print(f"Client {name} received: {response.message}")
        # Read the sender's name
        stay_connected = True
        while stay_connected:
            start_chat = input("Want to chat p2p?\n>:")
            if start_chat == "yes":
                print("Requesting possible chat...")
                request = server_pb2.ClientRequest(name=name)
                response = stub.Client(request)
                print(response.address_name)
                address_names = json.loads(response.address_name)
                print(address_names)
                selection_dict = {}
                for idx, (name, address) in enumerate(address_names.items()):
                    selection_dict[idx] = (name, address)
                    print(f"{idx}) {name}: {address}")
                chat_selection = input("Enter chat partners name: ")
                if chat_selection != "None":
                    with grpc.insecure_channel(selection_dict[int(chat_selection)][1]) as chat_channel:
                        chat_stub = chat_pb2_grpc.ChatStub(chat_channel)
                        print(f"P2P ChatRoom with {selection_dict[int(chat_selection)][0]}")
                        p2p_chat = True
                    while p2p_chat:




if __name__ == "__main__":
    name = sys.argv[1]
    port = sys.argv[2]
    main(name, port)
