# mocks/mock_server.py
"""Módulo que define un servidor mock usando Flask."""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/mock-endpoint", methods=["GET"])
def mock_endpoint():
    """Endpoint de prueba que devuelve datos simulados en formato JSON.

    Returns:
        Response: Respuesta JSON con estado 200 y datos simulados.
    """
    return jsonify({"success": True, "data": "Mock data"}), 200


if __name__ == "__main__":
    app.run(port=5000)
