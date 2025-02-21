# features/pages/api_test_page.py
"""Módulo que define las funciones para la funcionalidad del Test de APIs."""
import os

import requests
from dotenv import load_dotenv

from utils.error_dictionary import ErrorDictionary
from utils.logger import Logger

errors = ErrorDictionary()

load_dotenv()


class ApiTest:
    """Clase para pruebas de la API."""

    def __init__(self, context=None):
        """Inicializa la configuración de la API."""
        self.context = context
        self.API_URL = os.getenv("API_URL")
        self.TOKEN = context.token if context and hasattr(context, "token") else None
        self.items_request = (
            context.items_request
            if context and hasattr(context, "items_request")
            else None
        )
        self.logger = Logger().get_logger()

    async def test_login(self):
        """Prueba el endpoint de autenticación y obtiene el token."""
        response = requests.post(f"{self.API_URL}/login", json={})

        assert response.status_code == 200
        json_data = response.json()

        assert json_data["success"] is True
        assert "token" in json_data

        self.TOKEN = json_data["token"]
        self.logger.info(f"🔑 Token obtenido: {self.TOKEN}")

    async def test_get_items(self):
        """Prueba el endpoint GET /items."""
        headers = {"Authorization": f"Bearer {self.TOKEN}"}
        response = requests.get(f"{self.API_URL}/items", headers=headers)

        assert response.status_code == 200
        json_data = response.json()

        assert json_data["success"] is True
        assert isinstance(json_data["data"], list)

        self.items_request = json_data["data"]

        self.logger.info(f"📄 Se han obtenido todos los Items")
        self.logger.info(f"📄 Items: {json_data["data"][:3]}...")

    async def test_get_one_item(self, num):
        """Prueba el endpoint GET /items."""
        headers = {"Authorization": f"Bearer {self.TOKEN}"}
        response = requests.get(f"{self.API_URL}/items/{num}", headers=headers)

        assert response.status_code == 200
        json_data = response.json()

        assert json_data["success"] is True
        assert isinstance(json_data["data"], list)

    async def test_create_item(self, num: int):
        """Prueba la creación de un nuevo item con POST."""
        headers = {
            "Authorization": f"Bearer {self.TOKEN}",
            "Content-Type": "application/json",
        }

        new_item = {
            "id": num,
            "name": "Item de Prueba",
            "description": "Este es un item de prueba",
            "category": "Test",
            "price": 99.99,
            "stock": 10,
            "available": True,
        }

        response = requests.post(
            f"{self.API_URL}/items", json=new_item, headers=headers
        )

        assert response.status_code == 201
        json_data = response.json()

        assert json_data["success"] is True
        assert json_data["data"]["name"] == "Item de Prueba"

    async def test_update_item(self, num: int):
        """Prueba la actualización de un item con PUT."""
        headers = {
            "Authorization": f"Bearer {self.TOKEN}",
            "Content-Type": "application/json",
        }

        update_data = {"name": "Item Actualizado", "price": 120.50}

        response = requests.put(
            f"{self.API_URL}/items/{num}", json=update_data, headers=headers
        )

        assert response.status_code == 200
        json_data = response.json()

        assert json_data["success"] is True
        assert json_data["data"]["name"] == "Item Actualizado"
        assert json_data["data"]["price"] == 120.50

    async def test_delete_item(self, num: int):
        """Prueba la eliminación de un item con DELETE."""
        headers = {"Authorization": f"Bearer {self.TOKEN}"}
        response = requests.delete(f"{self.API_URL}/items/{num}", headers=headers)

        assert response.status_code == 200
        json_data = response.json()

        assert json_data["success"] is True
        assert json_data["message"] == "Item deleted"

    async def verify_items_request(self, data_table):
        """
        Verifica que en la lista de items (self.items_request) exista al menos un item
        que cumpla con los criterios especificados.

        - Para 'description': se verifica que contenga el texto indicado.
        - Para 'price' y 'stock': se permite usar condiciones del tipo '>100' o '<50' para comparaciones numéricas.
        - Para 'available': se realiza comparación insensible a mayúsculas.
        - Para el resto de campos se exige coincidencia exacta.

        data_table: lista de diccionarios con los criterios a buscar.
                    Los campos con valor vacío se ignoran.
        """
        if self.items_request is None:
            raise ValueError(
                "No se han obtenido los items. Ejecuta test_get_items antes de la verificación."
            )

        for criteria in data_table:
            matching_items = []
            for item in self.items_request:
                match = True
                for key, value in criteria.items():
                    value = value.strip()
                    if value:
                        item_value = item.get(key)
                        if item_value is None:
                            match = False
                            break

                        if key == "description":
                            if value not in str(item_value):
                                match = False
                                break

                        elif key in ["price", "stock"]:
                            if value.startswith(">") or value.startswith("<"):
                                operator = value[0]
                                try:
                                    threshold = float(value[1:])
                                    item_numeric = float(item_value)
                                except ValueError:
                                    match = False
                                    break
                                if operator == ">" and not (item_numeric > threshold):
                                    match = False
                                    break
                                if operator == "<" and not (item_numeric < threshold):
                                    match = False
                                    break
                            else:
                                try:
                                    if float(item_value) != float(value):
                                        match = False
                                        break
                                except ValueError:
                                    match = False
                                    break

                        elif key == "available":
                            if str(item_value).lower() != value.lower():
                                match = False
                                break

                        else:
                            if str(item_value) != value:
                                match = False
                                break
                if match:
                    matching_items.append(item)

            assert (
                matching_items
            ), f"No se encontró ningún item que cumpla con los criterios: {criteria}"
            self.logger.info(
                f"Para criterios 📥 {criteria} se encontraron los siguientes items: 📤 {matching_items}"
            )

        self.logger.info(
            "✅Todos los criterios se han verificado en los items obtenidos."
        )


"""
if scenario.status == "failed" or context.errors.has_errors():
        print(f"⚠️ El escenario '{scenario.name}' falló o acumuló errores.")
        context.loop.run_until_complete(take_screenshot(context.page, scenario.name))
    context.loop.run_until_complete(stop_tracing(context.browser_context))
    if context.errors.has_errors():
        for error in context.errors.get_all_errors():
            print(error)
        context.errors.clear_errors()
"""
