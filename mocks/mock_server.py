# mocks/mock_server.py
"""Módulo que define un servidor mock usando Flask con Swagger y persistencia en YAML.

En este mock se exige que todos los campos (id, name, description, category, price,
stock, available)
vengan informados (no vacíos) para que el endpoint /items devuelva 201. En caso de
que falte alguno,
o esté vacío, se devuelve un 400 (Bad Request). Si el id ya existe, devuelve 409.
"""

import secrets
from functools import wraps

import yaml
from flasgger import Swagger
from flask import Flask, jsonify, request

app = Flask(__name__)

# Configuración básica de Swagger
app.config["SWAGGER"] = {
    "title": "Mock TESTING API - Documentación",
    "description": "API para gestionar items simulados con persistencia en YAML.",
    "version": "1.0.1",
}
swagger = Swagger(app)

MOCK_FILE = "resources/mock_data.yaml"

# Generamos un token de ejemplo en el arranque
TOKEN = secrets.token_hex(16)


# Decorador para requerir token
def token_required(f):
    """Decorador que requiere la cabecera 'Authorization: Bearer <TOKEN>'."""

    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "Token faltante o inválido",
                    }
                ),
                401,
            )
        provided_token = auth_header.split("Bearer ")[-1]
        if provided_token != TOKEN:
            return jsonify({"success": False, "message": "Token inválido"}), 401
        return f(*args, **kwargs)

    return decorated


def load_mock_data():
    """Carga los datos desde el archivo YAML.

    Returns:
        list: Lista de items cargados desde el archivo YAML.
    """
    try:
        with open(MOCK_FILE, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
            return data.get("items", [])
    except (FileNotFoundError, yaml.YAMLError):
        return []


def save_mock_data(data):
    """Guarda los datos en el archivo YAML.

    Args:
        data (list): Lista de items.
    """
    with open(MOCK_FILE, "w", encoding="utf-8") as file:
        yaml.dump({"items": data}, file, default_flow_style=False, allow_unicode=True)


mock_data = load_mock_data()


@app.route("/login", methods=["POST"])
def login():
    """Autenticación sencilla para devolver un token de sesión.

    ---
    tags:
      - Auth
    parameters:
      - name: credentials
        in: body
        required: false
        schema:
          type: object
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Devuelve un token en caso de éxito.
        schema:
          type: object
          properties:
            success:
              type: boolean
            token:
              type: string
    """
    # (Podrías validar username/password en un entorno real)
    return jsonify({"success": True, "token": TOKEN}), 200


@app.route("/items", methods=["GET"])
@token_required
def get_items():
    """Devuelve la lista completa de items.

    ---
    tags:
      - Items
    responses:
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
@token_required
def get_item(item_id):
    """Obtiene un item específico por su ID.

    ---
    tags:
      - Items
    parameters:
      - name: item_id
        in: path
        type: integer
        required: true
        description: ID del item a buscar
    responses:
      200:
        description: Item encontrado
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              type: object
      404:
        description: Item no encontrado
    """
    item = next((i for i in mock_data if i["id"] == item_id), None)
    if item:
        return jsonify({"success": True, "data": item}), 200
    return jsonify({"success": False, "message": "Item not found"}), 404


@app.route("/items", methods=["POST"])
@token_required
def create_item():
    """Crea un nuevo item y lo agrega a la lista simulada.

    ---
    tags:
      - Items
    parameters:
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
    responses:
      201:
        description: Item creado exitosamente
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              type: object
      400:
        description: Datos inválidos
      409:
        description: ID duplicado
    """
    new_item = request.json
    # Cambios: validamos que vengan todos los campos y que no estén vacíos.
    required_fields = [
        "id",
        "name",
        "description",
        "category",
        "price",
        "stock",
        "available",
    ]
    for field in required_fields:
        # Verifica presencia y no-vacío
        if field not in new_item or not str(new_item[field]).strip():
            return (
                jsonify(
                    {"success": False, "message": f"Missing or invalid field '{field}'"}
                ),
                400,
            )

    # Verificar si el ID ya existe en la lista
    if any(i["id"] == new_item["id"] for i in mock_data):
        return jsonify({"success": False, "message": "Item ID already exists"}), 409
    
    # Si llega aquí, se asume que todos los campos son válidos
    mock_data.append(new_item)
    save_mock_data(mock_data)
    return jsonify({"success": True, "data": new_item}), 201


@app.route("/items/<int:item_id>", methods=["DELETE"])
@token_required
def delete_item(item_id):
    """Elimina un item de la lista basado en su ID.

    ---
    tags:
      - Items
    parameters:
      - name: item_id
        in: path
        type: integer
        required: true
        description: ID del item a eliminar
    responses:
      200:
        description: Item eliminado correctamente
      404:
        description: Item no encontrado
    """
    global mock_data
    item = next((i for i in mock_data if i["id"] == item_id), None)
    if not item:
        return jsonify({"success": False, "message": "Item not found"}), 404

    mock_data = [i for i in mock_data if i["id"] != item_id]
    save_mock_data(mock_data)
    return jsonify({"success": True, "message": "Item deleted"}), 200


@app.route("/items/<int:item_id>", methods=["PUT"])
@token_required
def put_item(item_id):
    """Actualiza un item existente en la lista.

    ---
    tags:
      - Items
    parameters:
      - name: item_id
        in: path
        type: integer
        required: true
        description: ID del item a actualizar
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
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
    responses:
      200:
        description: Item actualizado correctamente.
      400:
        description: Datos inválidos.
      404:
        description: Item no encontrado.
    """
    global mock_data
    item = next((i for i in mock_data if i["id"] == item_id), None)

    if not item:
        return jsonify({"success": False, "message": "Item not found"}), 404

    update_data = request.json
    if not update_data:
        return jsonify({"success": False, "message": "Invalid data"}), 400

    # Actualiza solo los campos que se envíen en la petición
    item.update(update_data)

    save_mock_data(mock_data)
    return (
        jsonify({"success": True, "message": f"Item {item_id} updated", "data": item}),
        200,
    )


if __name__ == "__main__":
    app.run(port=5000, debug=True)
