import json
from pathlib import Path, PurePath

import requests
from flask import Flask, request, send_from_directory, jsonify, abort
import os
from dotenv import dotenv_values

app = Flask(__name__)

API_KEY = dotenv_values(".env")["API_KEY"]
current_weather_url = "https://api.openweathermap.org/data/2.5/weather?"
forecast_weather_url = "http://api.openweathermap.org/data/2.5/forecast?"
geocoding_url = "http://api.openweathermap.org/geo/1.0/direct?q="


@app.route("/forecast", methods=["POST"])
def forecast():
    data = json.loads(request.get_json())
    print(data)
    if not data["type"] == "weather_request":
        abort(400, description="False request!")
    elif data["location"] == "location":
        abort(400, description="Please provide location!")
    elif data["time_frame"] == "empty":
        abort(400, description="Please provide time frame!")
    else:
        hours_forecasted = min(120, int(data["time_frame"]))
        hours_forecasted = hours_forecasted // 3
        hour_format = True if data["day_format"] == "hourly" else False
        geo_loc = requests.get(
            f"{geocoding_url}{data['location']}&limit=1&appid={API_KEY}"
        ).json()
        lat = geo_loc[0]["lat"]
        lon = geo_loc[0]["lon"]
        weather_forecast = requests.get(
            f"{forecast_weather_url}lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        ).json()
        if weather_forecast["cod"] != "200":
            abort(400, description="Server Problem2 :S")
        current_weather = requests.get(
            f"{current_weather_url}lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        ).json()
        if current_weather["cod"] != 200:
            abort(400, description="Server Problem3 :S")
        info_responds = build_responds(
            weather_forecast, current_weather, hours_forecasted, hour_format
        )
        return jsonify({"staus": "ok", "weather": info_responds}, 200)


def build_responds(weather_forecast, current_weather, hours_forecasted, hour_format):
    degree_sign = "\N{DEGREE SIGN}"
    current_condition = {
        "weather": current_weather["weather"][0]["description"],
        "temp": current_weather["main"]["temp"],
        "max_temp": current_weather["main"]["temp_max"],
        "min_temp": current_weather["main"]["temp_min"],
        "feel_temp": current_weather["main"]["feels_like"],
        "humidity": current_weather["main"]["humidity"],
        "wind": current_weather["wind"],
    }
    forecast_details = {
        "detail_lvl": "hourly" if hour_format else "daily",
        "station_name": current_weather["name"],
        "system": current_weather["sys"],
        "time": current_weather["dt"],
    }

    response = {
        "type": "weather_info",
        "location": weather_forecast["city"],
        "forecast_details": forecast_details,
        "time_frame": hours_forecasted,
        "current_condition": current_condition,
        "forecast": weather_forecast,
    }
    return response


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
