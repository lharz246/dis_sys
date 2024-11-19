import hashlib
import json
import sys
from pathlib import Path
from datetime import datetime
import colorama
import requests
import hashlib
import json
import os
from pathlib import Path
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
import requests

colorama.init()


def print_weather_info(weather_info):
    degree_sign = "\N{DEGREE SIGN}"
    hours_forecasted = weather_info["time_frame"]
    forecast_details = weather_info["forecast_details"]
    time_stamp = forecast_details["time"]
    timezone = forecast_details["timezone"]
    current_condition = weather_info["current_condition"]
    location = weather_info["location"]
    forecast = weather_info["forecast"]
    print(
        f"#########{Fore.GREEN}CURRENT WEATHER{Style.RESET_ALL}#########\n{location['name']}, {location['state']}, {location['country']}, {time_stamp}\n"
        f"currently: {Fore.MAGENTA}{current_condition['weather']}{Style.RESET_ALL} temperature: {Fore.GREEN}{current_condition['temp']}{degree_sign}C{Style.RESET_ALL}\n"
        f"feels_like: {Fore.YELLOW}{current_condition['feel_temp']}{Style.RESET_ALL} max_temp: {Fore.RED}{current_condition['max_temp']}{degree_sign}C{Style.RESET_ALL}\n"
        f"humidity: {Fore.BLUE}{current_condition['humidity']}{Style.RESET_ALL}  min_temp: {Fore.CYAN}{current_condition['temp']}{degree_sign}C{Style.RESET_ALL}\n"
    )
    for k, v in forecast.items():
        print(
            f"{location['name']}, {location['state']}, {location['country']}, {k}\n"
            f"Temperature: {Fore.MAGENTA}{v['weather']}{Style.RESET_ALL} temperature: {Fore.GREEN}{v['temp']}{degree_sign}C{Style.RESET_ALL}\n"
            f"feels_like: {Fore.YELLOW}{v['feel_temp']}{Style.RESET_ALL} max_temp: {Fore.RED}{v['max_temp']}{degree_sign}C{Style.RESET_ALL}\n"
            f"humidity: {Fore.BLUE}{v['humidity']}{Style.RESET_ALL}  min_temp: {Fore.CYAN}{v['temp']}{degree_sign}C{Style.RESET_ALL}\n"
        )


class SimpleClient:
    def __init__(self, server_address, port):
        self.server_address = server_address
        self.port = port

    def get_weather_info(self, city, time_frame, hourly):
        with open("skeleton.json") as file:
            weather_request = json.load(file)
        weather_request["type"] = "weather_request"
        weather_request["location"] = city
        weather_request["time_frame"] = time_frame
        weather_request["day_format"] = hourly
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
        time_frame = int(sys.argv[2])
        client.get_weather_info(
            city, time_frame, True if sys.argv[3] == "hourly" else False
        )
