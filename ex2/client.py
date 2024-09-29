import os
from pathlib import Path
import json
import requests
import sys

class SimpleClient:
    def __init__(self, cache_dir, server_address, port, commands):
        self.cache_dir = os.path.join(os.path.dirname(__file__), cache_dir)
        self.server_address = server_address
        self.port = port
        self.cached_files = []
        self.commands = commands

    def send_file(self, file_name):
        file_content = Path(f"{self.cache_dir}/{file_name}").read_text()
        base_file_name, _ = os.path.splitext(file_name)
        file_payload = {"filename": base_file_name, "object": file_content, "extension": "txt"}
        response = requests.post(
            f"http://{self.server_address}:{self.port}/upload", json=json.dumps(file_payload)
        )
        print(response)

    def receive_file(self, file_name):
        try:
            local_file_path = Path(f"{self.cache_dir}/{file_name}")
            if local_file_path.exists():
                print(f"{file_name} exists locally.")
                return local_file_path.read_text()

            response = requests.get(f"http://{self.server_address}:{self.port}/{file_name}")
            if response.status_code == 200:
                file_content = response.text
                with local_file_path.open("w") as f:
                    f.write(file_content)
                print(f"{file_name} downloaded and saved locally.")
                return file_content
            else:
                print(f"Error: unable to download {file_name} from server.")
        except Exception as e:
            print(f"Error while downloading file: {e}")

    def get_dir_tree(self):
        pass

    def run_client(self):
        while True:
            user_input = input().split()
            if user_input[0] not in self.commands or len(user_input) not in [1, 2]:
                print("Unknown command! Available commands: <send>, <receive>")
            elif len(user_input) == 1:
                return self.get_dir_tree()
            elif user_input[0] == "send":
                return self.send_file(user_input[1])
            elif user_input[0] == "open":
                return self.receive_file(user_input[1])
            else:
                break
        print("Shutting down client!")

if __name__ == "__main__":
    client = SimpleClient(
        cache_dir="client_storage",
        commands=["open", "send", "ll"],
        server_address="127.0.0.1",
        port=5000,
    )

    if len(sys.argv) > 1:
        file_to_download = sys.argv[1]
        client.receive_file(file_to_download)
    else:
        print("Please specify the file name to download as an argument.")
