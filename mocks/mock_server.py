# mocks/mock_server.py
"""Módulo que define un servidor mock usando Flask con persistencia de datos en YAML."""

import yaml
from flask import Flask, jsonify, request

app = Flask(__name__)

MOCK_FILE = "resources/mock_data.yaml"  # Ruta del archivo YAML


# ------------------------------
# Función para cargar datos desde el archivo YAML
# ------------------------------
def load_mock_data():
    """Carga los datos desde el archivo YAML."""
    try:
        with open(MOCK_FILE, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
            return data.get("items", [])  # Retorna la lista de items
    except (FileNotFoundError, yaml.YAMLError):
        return []  # Si el archivo no existe o está corrupto, devuelve una lista vacía


# ------------------------------
# Función para guardar datos en el archivo YAML
# ------------------------------
def save_mock_data(data):
    """Guarda los datos en el archivo YAML."""
    with open(MOCK_FILE, "w", encoding="utf-8") as file:
        yaml.dump({"items": data}, file, default_flow_style=False, allow_unicode=True)


# Cargar datos en memoria al iniciar
mock_data = load_mock_data()


# ------------------------------
# GET - Obtener todos los items
# ------------------------------
@app.route("/items", methods=["GET"])
def get_items():
    """Devuelve la lista completa de items almacenados en el servidor."""
    return jsonify({"success": True, "data": mock_data}), 200


# ------------------------------
# GET - Obtener un item por ID
# ------------------------------
@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    """Obtiene un item específico por su ID."""
    item = next((i for i in mock_data if i["id"] == item_id), None)
    if item:
        return jsonify({"success": True, "data": item}), 200
    return jsonify({"success": False, "message": "Item not found"}), 404


# ------------------------------
# POST - Crear un nuevo item
# ------------------------------
@app.route("/items", methods=["POST"])
def create_item():
    """Crea un nuevo item y lo agrega a la lista simulada."""
    new_item = request.json  # Captura datos enviados en la solicitud

    # Validar estructura de datos
    if not new_item or "id" not in new_item or "name" not in new_item:
        return jsonify({"success": False, "message": "Invalid data"}), 400

    # Prevenir duplicados
    if any(i["id"] == new_item["id"] for i in mock_data):
        return jsonify({"success": False, "message": "Item ID already exists"}), 409

    mock_data.append(new_item)  # Agregar el nuevo item
    save_mock_data(mock_data)  # Guardar cambios en YAML
    return jsonify({"success": True, "data": new_item}), 201


# ------------------------------
# PUT - Actualizar un item existente
# ------------------------------
@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    """Actualiza un item existente basado en su ID."""
    item = next((i for i in mock_data if i["id"] == item_id), None)

    if not item:
        return jsonify({"success": False, "message": "Item not found"}), 404

    data = request.json  # Captura datos enviados en la solicitud

    # Validar datos recibidos
    if not data or "name" not in data:
        return jsonify({"success": False, "message": "Invalid data"}), 400

    item.update(data)  # Actualizar datos
    save_mock_data(mock_data)  # Guardar cambios en YAML
    return jsonify({"success": True, "data": item}), 200


# ------------------------------
# DELETE - Eliminar un item
# ------------------------------
@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    """Elimina un item de la lista basado en su ID."""
    global mock_data
    item = next((i for i in mock_data if i["id"] == item_id), None)

    if not item:
        return jsonify({"success": False, "message": "Item not found"}), 404

    mock_data = [i for i in mock_data if i["id"] != item_id]  # Filtrar lista
    save_mock_data(mock_data)  # Guardar cambios en YAML
    return jsonify({"success": True, "message": "Item deleted"}), 200


# ------------------------------
# Punto de entrada del servidor Flask
# ------------------------------
if __name__ == "__main__":
    app.run(port=5000, debug=True)
