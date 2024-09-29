import json
from pathlib import Path, PurePath
from flask import Flask, request, send_from_directory, jsonify, abort
import os

STORAGE_PATH = f"{Path.cwd()}/server_storage"
if Path(f"{STORAGE_PATH}/file_index/index.json").is_file():
    with open(f"{STORAGE_PATH}/file_index/index.json", "r") as f:
        uploaded_files = json.loads(f.read())
else:
    uploaded_files = {}
app = Flask(__name__)

print(uploaded_files)


@app.route("/")
def starting():
    greeting = (
        "Hello! This is our small and simple file server. "
        "It allows the user to save files remotely and "
        "enables the user to work with these files as they "
        "were locally saved, therefore ensuring network transparency"
    )
    return jsonify(greeting)


@app.route("/upload", methods=["POST"])
def upload_file():
    if request.is_json:
        request_object = json.loads(request.get_json())
        print(f"received:{request_object}")
        print(request_object)
        print(type(request_object))
        file_name = request_object.get("filename")
        if not file_name:
            abort(400, description="Filename is missing.")
        path = request_object.get("path")
        file_hash = request_object.get("hash")
        print(file_hash)
        with open(f"{STORAGE_PATH}/{file_hash}.json", "w") as f:
            json.dump(request_object, f)
        uploaded_files[f"{file_hash}"] = {
            "file": f"{STORAGE_PATH}/{file_name}.json",
            "path": path,
        }
        with open(f"{STORAGE_PATH}/file_index/index.json", "w") as f:
            json.dump(uploaded_files, f)
            print(uploaded_files)
            return jsonify({"status": "success", "file": file_name}), 200
    return jsonify({"error": "This endpoint only supports POST with JSON data."}), 400


@app.route("/<filename>", methods=["GET"])
def send_file(filename):
    file_path = PurePath(STORAGE_PATH, f"{filename}.json")
    print(file_path)
    if Path(file_path).is_file():
        print("HiEr1")
        if filename not in uploaded_files:
            uploaded_files[filename] = file_path
        return send_from_directory(STORAGE_PATH, f"{filename}.json", as_attachment=True)
    else:
        abort(404, description=f"File '{filename}' not found.")


@app.get("/directories")
def list_uploaded_files():
    return jsonify(uploaded_files)


if __name__ == "__main__":
    if not os.path.exists(STORAGE_PATH):
        os.makedirs(STORAGE_PATH)
    if not os.path.exists(f"{STORAGE_PATH}/file_index"):
        os.makedirs(f"{STORAGE_PATH}/file_index")

    app.run(host="127.0.0.1", port=5000, debug=False)
