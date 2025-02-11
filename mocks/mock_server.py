# mocks/mock_server.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/mock-endpoint', methods=['GET'])
def mock_endpoint():
    return jsonify({"success": True, "data": "Mock data"}), 200

if __name__ == "__main__":
    app.run(port=5000)
