import datetime
import json
import math
from datetime import datetime, timedelta
import requests
from flask import Flask, request, jsonify, abort
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

        hour_format = data["day_format"]
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
            weather_forecast,
            current_weather,
            geo_loc[0],
            data["time_frame"],
            hour_format,
        )
        return jsonify({"staus": "ok", "weather": info_responds}, 200)


def build_responds(
    weather_forecast,
    current_weather,
    geo_data,
    time_frame,
    hour_format,
):

    request_time = datetime.fromtimestamp(current_weather["dt"])
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
        "time": request_time.strftime("%d-%m-%Y"),
        "timezone": current_weather["timezone"],
    }
    forecast_data = {}
    if hour_format:
        offset = 1 if request_time.hour % 3 == 0 else 0
        data_points = math.ceil(time_frame / 3)
        weather_data = weather_forecast["list"][offset : data_points + offset]
        idx = 0
        for i in range(time_frame):
            forecast_data[
                f"{(request_time + timedelta(hours=i + offset)).strftime('%d-%m-%Y %H:%M:%S')}"
            ] = {
                "weather": weather_data[idx]["weather"][0]["description"],
                "temp": weather_data[idx]["main"]["temp"],
                "max_temp": weather_data[idx]["main"]["temp_max"],
                "min_temp": weather_data[idx]["main"]["temp_min"],
                "feel_temp": weather_data[idx]["main"]["feels_like"],
                "humidity": weather_data[idx]["main"]["humidity"],
                # "wind": weather_data[idx]["wind"],
            }
            if math.ceil(i / 3) > 1:
                idx += 1
    else:
        starting_day = (request_time + timedelta(days=1)).date()
        delta = (
            datetime.combine(starting_day, datetime.min.time()) - request_time
        ).seconds / 10800
        offset = math.floor(delta) if request_time.hour % 3 == 0 else math.ceil(delta)
        data_points = time_frame * 8
        weather_data = weather_forecast["list"][offset : data_points + offset]
        counter = 0
        weather_list = []
        temp_list = []
        max_temp = 0
        min_temp = 100
        feel_temp_list = []
        humiditiy_list = []
        key = starting_day
        for data in weather_data:
            if data["weather"][0]["description"] not in weather_list:
                weather_list.append(data["weather"][0]["description"])
            temp_list.append(data["main"]["temp"])
            feel_temp_list.append(data["main"]["feels_like"])
            humiditiy_list.append(data["main"]["humidity"])
            if data["main"]["temp_max"] > max_temp:
                max_temp = data["main"]["temp_max"]
            if data["main"]["temp_min"] < min_temp:
                min_temp = data["main"]["temp_min"]
            counter += 1
            if counter % 8 == 0 and counter:
                forecast_data[f"{key}"] = {
                    "weather": weather_list,
                    "temp": sum(temp_list) / float(len(temp_list)),
                    "max_temp": max_temp,
                    "min_temp": min_temp,
                    "feel_temp": sum(feel_temp_list) / float(len(feel_temp_list)),
                    "humidity": sum(humiditiy_list) / float(len(humiditiy_list)),
                    # "wind": [],
                }
                weather_list = []
                temp_list = []
                max_temp = 0
                min_temp = 100
                feel_temp_list = []
                humiditiy_list = []
                key = datetime.fromtimestamp(data["dt"]).date()

    response = {
        "type": "weather_info",
        "location": {
            "name": geo_data["name"],
            "state": geo_data["state"],
            "country": geo_data["country"],
        },
        "forecast_details": forecast_details,
        "time_frame": time_frame,
        "current_condition": current_condition,
        "forecast": forecast_data,
    }
    return response


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
