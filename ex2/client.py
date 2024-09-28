import json
from pathlib import Path

import requests


class SimpleClient:
    def __init__(self, cache_dir, server_address, port, commands):
        self.cache_dir = cache_dir
        self.server_address = server_address
        self.port = port
        self.cached_files = []
        self.commands = commands

    def send_file(self, file_name):
        file = Path(f"{self.cache_dir}/{file_name}").read_text()
        file_name, extension = file_name.split(".")
        object_dict = {"filename": file_name, "object": file, "extension": "txt"}
        object_json = json.dumps(object_dict)
        respond = requests.post(
            f"http://{self.server_address}:{self.port}/upload", json=object_json
        )
        print(respond)

    def receive_file(self, file_name):
        pass

    def get_dir_tree(self):
        pass

    def run_client(self):
        while True:
            request = input()
            input_cmd = request.split()
            if (
                input_cmd[0] not in self.commands
                or len(input_cmd) < 1
                or len(input_cmd) > 2
            ):
                print("Unknown command! available commands: <send>, <receive>")
            elif len(input_cmd) == 1:
                return self.get_dir_tree()
            elif input_cmd[0] == "send":
                return self.send_file(input_cmd[1])
            elif input_cmd[0] == "open":
                return self.receive_file(input_cmd[1])
            else:
                break
        print("Shutting down client!")


cl = SimpleClient(
    cache_dir="/home/leon/Schreibtisch/dis_sys/ex2/client_storage",
    commands=["open", "send", "ll"],
    server_address="127.0.0.1",
    port=5000,
)

cl.send_file("test2.txt")
