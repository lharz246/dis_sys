import hashlib
import json
import sys
from pathlib import Path
import requests
import hashlib
import json
import os
from pathlib import Path

import requests


def print_weather_info(weather_info):
    current_condition = weather_info["current_condition"]
    print(current_condition)
    print("#" * 20)
    print(weather_info["forecast"])


class SimpleClient:
    def __init__(self, cache_dir, server_address, port):
        self.cache_dir = os.path.join(os.path.dirname(__file__), cache_dir)
        self.server_address = server_address
        self.port = port

    def get_weather_info(self, city, time_frame, hourly):
        with open("skeleton.json") as file:
            weather_request = json.load(file)
        weather_request["type"] = "weather_request"
        weather_request["location"] = city
        weather_request["time_frame"] = time_frame
        weather_request["day_format"] = 0 if hourly else 1
        weather_request = json.dumps(weather_request)
        response = requests.post(
            f"http://{self.server_address}:{self.port}/forecast", json=weather_request
        )
        if response.status_code == 200:
            weather_info = json.loads(response.text)[0]["weather"]
            print_weather_info(weather_info)
        else:
            print(f"Server problems :S")


if __name__ == "__main__":
    client = SimpleClient(
        cache_dir="client_storage",
        server_address="127.0.0.1",
        port=5000,
    )
    if len(sys.argv) != 4:
        print("Usage: python client.py <city> <time_frame> <daily||hourly>")
        sys.exit(1)
    elif sys.argv[3] != "daily" and sys.argv[3] != "hourly":
        print("ll Usage: python client.py <city> <time_frame> <daily||hourly>")
        sys.exit(1)
    else:
        city = sys.argv[1]
        time_frame = (
            int(sys.argv[2]) if sys.argv[3] == "hourly" else int(sys.argv[2]) * 24
        )
        client.get_weather_info(
            city, time_frame, True if sys.argv[3] == "hourly" else False
        )
