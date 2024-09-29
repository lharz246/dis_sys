import os
import json
from flask import Flask, request, send_from_directory, jsonify, abort

STORAGE_PATH = os.path.join(os.path.dirname(__file__), "server_storage")
uploaded_files = {}
app = Flask(__name__)

@app.route("/")
def home():
    return "<p>Hello, World!</p>"

@app.route("/upload", methods=["POST"])
def upload_file():
    if request.is_json:
        data = request.get_json()
        print("Received payload:", data)  # Debugging: Print received payload

        file_name = data.get("filename")
        file_content = data.get("object")

        # Empty content is acceptable, but filename is still required
        if not file_name:
            abort(400, description="Filename is missing.")

        file_path = os.path.join(STORAGE_PATH, f"{file_name}.json")
        with open(file_path, "w") as file:
            json.dump(file_content, file)  # Store empty string if content is empty

        uploaded_files[file_name] = file_path
        return jsonify({"status": "success", "file": file_name}), 200
    return jsonify({"error": "This endpoint only supports POST with JSON data."}), 400

@app.route("/<filename>", methods=["GET"])
def send_file(filename):
    file_path = os.path.join(STORAGE_PATH, filename)

    if os.path.exists(file_path):
        if filename not in uploaded_files:
            uploaded_files[filename] = file_path

        return send_from_directory(STORAGE_PATH, filename, as_attachment=True)
    else:
        abort(404, description=f"File '{filename}' not found.")

@app.get("/directories")
def list_uploaded_files():
    return jsonify(uploaded_files)

if __name__ == "__main__":
    if not os.path.exists(STORAGE_PATH):
        os.makedirs(STORAGE_PATH)
    
    app.run(host="127.0.0.1", port=5000, debug=True)
