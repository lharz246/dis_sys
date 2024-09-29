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
      
        file_path = Path(f"{self.cache_dir}/{file_name}")
        if not file_path.exists():
            print(f"Error: {file_name} does not exist in the client storage.")
            return

  
        try:
            file_content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"Error reading file {file_name}: {e}")
            return

        base_file_name, _ = os.path.splitext(file_name)

       
        file_payload = {
            "filename": base_file_name,   
            "object": file_content        
        }

        print("Sending payload:", file_payload)  
        response = requests.post(
            f"http://{self.server_address}:{self.port}/upload", json=file_payload
        )

        if response.status_code == 200:
            print(f"File '{file_name}' successfully uploaded.")
        else:
            print(f"Error uploading file: {response.text}")

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
                print(f"Error: unable to download {file_name} from server. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error while downloading file: {e}")

if __name__ == "__main__":
    client = SimpleClient(
        cache_dir="client_storage",
        server_address="127.0.0.1",
        port=5000,
        commands=["upload", "download"]
    )

    if len(sys.argv) < 3:
        print("Usage: python client.py <upload/download> <filename>")
        sys.exit(1)

    command = sys.argv[1]
    file_name = sys.argv[2]

    if command == "upload":
        client.send_file(file_name)
    elif command == "download":
        client.receive_file(file_name)
    else:
        print("Unknown command! Use 'upload' or 'download'.")
