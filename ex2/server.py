import json

from flask import Flask, request, send_from_directory, jsonify

STORAGE_PATH = "/home/leon/Schreibtisch/dis_sys/ex2/storage"
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
            request_object = request.get_json()
            file_path = request_object["file_path"]
            file_name = request_object["filename"]
            file = request_object["object"]
            f = request.files["test"]
            with open(f"{file_path}/{file_name}.json", "w") as f:
                json.dump(file, f)
            directories[f"{file_path}/{file_name}"] = file_name


@app.route("/<filename>", methods=["GET"])
def send_file(filename):
    return send_from_directory("storage", filename, as_attachment=True)


@app.get("/directories")
def get_directories():
    return jsonify(directories)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
