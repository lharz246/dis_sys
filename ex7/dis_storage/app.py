from dapr.clients import DaprClient
from flask import Flask, request, jsonify
import sys

app = Flask(__name__)

keys_list = []


@app.route("/store", methods=["POST"])
def store_data():
    data = request.json
    key = data["key"]
    value = data["value"]
    with DaprClient() as client:
        print(f"Storing data -> Key: {key}, Value: {value}")
        client.save_state(store_name="statestore", key=key, value=value)
        keys_list.append(key)
    return jsonify({"status": "saved", "key": key})


@app.route("/retrieve/<key>", methods=["GET"])
def retrieve_data(key):
    with DaprClient() as client:
        result = client.get_state(store_name="statestore", key=key)
    print(f"Retrieved data -> Key: {key}, Value: {result.data}")
    return jsonify({"key": key, "value": result.data.decode() if result.data else None})


if __name__ == "__main__":
    app.run(port=5000)
