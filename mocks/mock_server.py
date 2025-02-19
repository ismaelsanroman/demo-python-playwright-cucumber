# mocks/mock_server.py
"""Módulo define un servidor mock usando Flask con Swagger y persistencia en YAML."""

import yaml
from flasgger import Swagger
from flask import Flask, jsonify, request

app = Flask(__name__)

# Configuración básica de Swagger
app.config["SWAGGER"] = {
    "title": "Mock API - Documentación",
    "description": "API para gestionar items simulados con persistencia en YAML.",
    "version": "1.0.0",
}
swagger = Swagger(app)

MOCK_FILE = "mocks/mock_data.yaml"  # Ruta del archivo YAML


def load_mock_data():
    """Carga los datos desde el archivo YAML.

    Returns:
        list: Lista de items cargados desde el archivo YAML.
    """
    try:
        with open(MOCK_FILE, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
            return data.get("items", [])  # Retorna la lista de items
    except (FileNotFoundError, yaml.YAMLError):
        # Si el archivo no existe o está corrupto, devuelve una lista vacía
        return []


def save_mock_data(data):
    """Guarda los datos en el archivo YAML.

    Args:
        data (list): Lista de items a guardar en el archivo YAML.
    """
    with open(MOCK_FILE, "w", encoding="utf-8") as file:
        yaml.dump({"items": data}, file, default_flow_style=False, allow_unicode=True)


# Cargamos los datos en memoria al iniciar
mock_data = load_mock_data()


@app.route("/items", methods=["GET"])
def get_items():
    """Devuelve la lista completa de items almacenados en el servidor.

    Returns:
        dict: Respuesta con la lista de items.

    Swagger responses:
      200:
        description: Lista de items obtenida correctamente.
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              type: array
              items:
                type: object
    """
    return jsonify({"success": True, "data": mock_data}), 200


@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    """Obtiene un item específico por su ID.

    Args:
        item_id (int): ID del item a buscar.

    Returns:
        dict: Respuesta con el item encontrado o mensaje de error.

    Swagger parameters:
      - name: item_id
        in: path
        type: integer
        required: true
        description: ID del item a buscar.

    Swagger responses:
      200:
        description: Item encontrado.
      404:
        description: Item no encontrado.
    """
    item = next((i for i in mock_data if i["id"] == item_id), None)
    if item:
        return jsonify({"success": True, "data": item}), 200
    return jsonify({"success": False, "message": "Item not found"}), 404


@app.route("/items", methods=["POST"])
def create_item():
    """Crea un nuevo item y lo agrega a la lista simulada.

    Returns:
        dict: Respuesta con el item creado o mensaje de error.

    Swagger parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
            description:
              type: string
            category:
              type: string
            price:
              type: number
            stock:
              type: integer
            available:
              type: boolean

    Swagger responses:
      201:
        description: Item creado exitosamente.
      400:
        description: Datos inválidos.
      409:
        description: ID duplicado.
    """
    new_item = request.json

    if not new_item or "id" not in new_item or "name" not in new_item:
        return jsonify({"success": False, "message": "Invalid data"}), 400

    if any(i["id"] == new_item["id"] for i in mock_data):
        return jsonify({"success": False, "message": "Item ID already exists"}), 409

    mock_data.append(new_item)
    save_mock_data(mock_data)
    return jsonify({"success": True, "data": new_item}), 201


@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    """Elimina un item de la lista basado en su ID.

    Args:
        item_id (int): ID del item a eliminar.

    Returns:
        dict: Mensaje de éxito o error.

    Swagger parameters:
      - name: item_id
        in: path
        type: integer
        required: true

    Swagger responses:
      200:
        description: Item eliminado correctamente.
      404:
        description: Item no encontrado.
    """
    global mock_data
    item = next((i for i in mock_data if i["id"] == item_id), None)

    if not item:
        return jsonify({"success": False, "message": "Item not found"}), 404

    mock_data = [i for i in mock_data if i["id"] != item_id]
    save_mock_data(mock_data)
    return jsonify({"success": True, "message": "Item deleted"}), 200


if __name__ == "__main__":
    app.run(port=5000, debug=True)
