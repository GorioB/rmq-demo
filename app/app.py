from flask import Flask, request, jsonify
from .process_data import process_data
from .publish_result import publish_result

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/publish", methods=["POST"])
def publish():
    data = request.json  # used json input just cause
    processed_data = process_data(data)
    publish_result(processed_data)
    return jsonify({
        "published_result": data
    })
