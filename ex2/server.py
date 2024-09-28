import json

from flask import Flask, request, send_from_directory, jsonify

STORAGE_PATH = "/home/leon/Schreibtisch/dis_sys/ex2/server_storage"
filename = "test.txt"
directories = {"storage": "test.txt"}
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if request.is_json:
            request_object = json.loads(request.get_json())
            print(request_object)
            print(type(request_object))
            file_name = request_object["filename"]
            file = request_object["object"]
            with open(f"{STORAGE_PATH}/{file_name}.json", "w") as f:
                json.dump(file, f)
            directories[f"{file_name}"] = f"{STORAGE_PATH}/{file_name}.json"
            return jsonify("success")


@app.route("/<filename>", methods=["GET"])
def send_file(filename):
    return send_from_directory("storage", directories[filename], as_attachment=True)


@app.get("/directories")
def get_directories():
    return jsonify(directories)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
