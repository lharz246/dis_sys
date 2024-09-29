import hashlib
import json
import os
from pathlib import Path

import requests

STORAGE_PATH = f"{Path.cwd()}/client_storage"


class SimpleClient:
    def __init__(self, cache_dir, server_address, port):
        self.cache_dir = os.path.join(os.path.dirname(__file__), cache_dir)
        self.server_address = server_address
        self.port = port
        self.cached_files = [
            f for f in Path(f"{Path.cwd()}/client_storage").iterdir() if f.is_file()
        ]

    def send_file(self, file_name):
        path = Path(f"{self.cache_dir}/{file_name}")
        if not path.is_file():
            print(f"Error: {file_name} does not exist in the client storage.")
            return
        try:
            file = path.read_text()
        except Exception as e:
            print(f"Error reading file {file_name}: {e}")
            return
        hash_func = hashlib.sha256()
        hash_func.update(bytes(f"{Path.cwd()}/{file_name}", encoding="utf-8"))
        file_hash = hash_func.hexdigest()
        object_dict = {
            "filename": file_name,
            "object": file,
            "extension": "txt",
            "path": str(Path.cwd()),
            "hash": file_hash,
        }
        object_json = json.dumps(object_dict)
        response = requests.post(
            f"http://{self.server_address}:{self.port}/upload", json=object_json
        )
        if response.status_code == 200:
            print(f"File '{file_name}' successfully uploaded.")
        else:
            print(f"Error uploading file: {response.text}")

    def receive_file(self, cmd, file_name):
        try:
            local_file_path = Path(f"{self.cache_dir}/{file_name}")
            if Path(f"{self.cache_dir}/{file_name}").is_file():
                return os.system(f"{cmd} {self.cache_dir}/{file_name}")
            hash_func = hashlib.sha256()
            hash_func.update(bytes(f"{Path.cwd()}/{file_name}", encoding="utf-8"))
            file_hash = hash_func.hexdigest()
            response = requests.get(
                f"http://{self.server_address}:{self.port}/{file_hash}"
            )
            print(response.text)
            if response.status_code == 200:
                file_content = json.loads(response.text)["object"]
                with local_file_path.open("w") as f:
                    f.write(file_content)
                return os.system(f"{cmd} {self.cache_dir}/{file_name}")
            else:
                print(
                    f"Error: unable to download {file_name} from server. Status code: {response.status_code}"
                )
        except Exception as e:
            print(f"Error while downloading file: {e}")

    def run(self):
        while True:
            print(">:", end="")
            cmd = input()
            cmd = cmd.split(" ")
            if cmd[0] == "":
                pass
            elif cmd[0] == "send":
                self.send_file(cmd[1])
            elif cmd[0] == "exit":
                print("Shutting down client!")
                break
            else:
                print(f"{cmd[0]} {cmd[1]}")
                self.receive_file(cmd[0], cmd[1])


if __name__ == "__main__":
    if not os.path.exists(STORAGE_PATH):
        os.makedirs(STORAGE_PATH)
    client = SimpleClient(
        cache_dir="client_storage",
        server_address="127.0.0.1",
        port=5000,
    )

    client.run()
    # if len(sys.argv) < 3:
    #     print("Usage: python client.py <upload/download> <filename>")
    #     sys.exit(1)
    #
    # command = sys.argv[1]
    # file_name = sys.argv[2]
    #
    # if command == "upload":
    #     client.send_file(file_name)
    # elif command == "download":
    #     client.receive_file(file_name)
    # else:
    #     print("Unknown command! Use 'upload' or 'download'.")
