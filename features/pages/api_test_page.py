# features/pages/api_test_page.py
"""Módulo que define los steps para la funcionalidad de API_TEST en BDD."""

import os

import requests
from dotenv import load_dotenv

from utils.error_dictionary import ErrorDictionary
from utils.logger import Logger

errors = ErrorDictionary()
load_dotenv()


class ApiTest:
    """Clase para pruebas de la API.

    Esta clase implementa funciones para realizar pruebas de endpoints de la API,
    incluyendo login, obtención de items, creación, verificación y eliminación.
    """

    def __init__(self, context=None):
        """Inicializa la configuración de la API.

        Args:
            context: Contexto de ejecución que puede contener token e items.
        """
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
        """Realiza la petición POST al endpoint /login para obtener el token.

        Registra el token obtenido con el icono 🔑.
        """
        response = requests.post(f"{self.API_URL}/login", json={})
        assert response.status_code == 200
        json_data = response.json()
        assert json_data["success"] is True
        assert "token" in json_data
        self.TOKEN = json_data["token"]
        self.logger.info(f"🔑 Token obtenido: {self.TOKEN}")

    async def test_get_items(self):
        """Realiza la petición GET al endpoint /items para obtener la lista de items.

        Registra la acción y muestra los primeros 3 items con el icono 📄.
        """
        headers = {"Authorization": f"Bearer {self.TOKEN}"}
        response = requests.get(f"{self.API_URL}/items", headers=headers)
        assert response.status_code == 200
        json_data = response.json()
        assert json_data["success"] is True
        assert isinstance(json_data["data"], list)
        self.items_request = json_data["data"]
        self.logger.info("📄 Se han obtenido todos los Items")
        self.logger.info(f"📄 Items: {json_data['data'][:3]}...")

    async def verify_items_request(self, data_table):
        """Verifica que la lista de items cumpla con los criterios especificados.

        - Para 'description': se verifica que contenga el texto indicado.
        - Para 'price' y 'stock': se permite usar operadores como '>100' o '<50'.
        - Para 'available': se realiza comparación insensible a mayúsculas.
        - Para los demás campos: se exige coincidencia exacta.

        Se registran los resultados con iconos para facilitar el debug.
        """
        if self.items_request is None:
            raise ValueError(
                "No se han obtenido los items. Ejecute test_get_items primero."
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
            ), f"❌ No se encontró ningún item con los criterios: {criteria}"
            self.logger.info(f"📥 Criterios {criteria} -> Items: {matching_items}")
        self.logger.info(
            "✅ Todos los criterios se han verificado en los items obtenidos."
        )

    async def test_create_item_from_params(self, params: dict):
        """Envía una petición POST para crear un item con los parámetros dados.

        Convierte los tipos (id, price, stock y available) y verifica que la respuesta
        sea correcta. Registra el proceso con iconos 🚀 y ✅.
        """
        headers = {
            "Authorization": f"Bearer {self.TOKEN}",
            "Content-Type": "application/json",
        }
        try:
            params["id"] = int(params["id"])
            params["price"] = float(params["price"])
            params["stock"] = int(params["stock"])
            if isinstance(params["available"], str):
                params["available"] = params["available"].lower() == "true"
        except Exception as e:
            self.logger.error(f"❌ Error al convertir parámetros: {e}")
            raise

        self.logger.info(f"🚀 Creando item con parámetros: {params}")
        response = requests.post(f"{self.API_URL}/items", json=params, headers=headers)
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        json_data = response.json()
        assert json_data["success"] is True, f"❌ Fallo en la creación: {json_data}"
        assert (
            json_data["data"]["name"] == params["name"]
        ), "❌ El nombre del item creado no coincide"
        self.logger.info(f"✅ Item creado: {json_data['data']}")

    async def verify_created_item(self, item_id):
        """Verifica que el item creado con el ID indicado existe.

        Realiza una petición GET a /items/{id} y registra la respuesta con iconos 🚀 y ✅.
        """
        headers = {"Authorization": f"Bearer {self.TOKEN}"}
        self.logger.info(f"🚀 Verificando item con ID: {item_id}")
        response = requests.get(f"{self.API_URL}/items/{item_id}", headers=headers)
        assert response.status_code == 200, (
            f"❌ Error al obtener el item creado: status code " f"{response.status_code}"
        )
        json_data = response.json()
        assert json_data["success"] is True, f"❌ Error al obtener el item: {json_data}"
        self.logger.info(f"✅ Item verificado: {json_data['data']}")

    async def test_delete_item(self, item_id: int):
        """Envía una petición DELETE para eliminar el item con el ID especificado.

        Registra el proceso con iconos 🚀 y ✅.
        """
        headers = {"Authorization": f"Bearer {self.TOKEN}"}
        self.logger.info(f"🚀 Enviando DELETE para el item con ID: {item_id}")
        response = requests.delete(f"{self.API_URL}/items/{item_id}", headers=headers)
        assert (
            response.status_code == 200
        ), f"❌ Error al borrar el item: status code {response.status_code}"
        json_data = response.json()
        assert json_data["success"] is True, f"❌ Fallo en la eliminación: {json_data}"
        assert (
            json_data["message"] == "Item deleted"
        ), "❌ Mensaje de eliminación inesperado"
        self.logger.info(f"✅ Item con ID {item_id} eliminado correctamente.")

    async def delete_created_items(self, item_ids):
        """Envía peticiones DELETE para cada item en la lista de IDs.

        Este método soporta borrar uno o varios elementos, registrando cada borrado.
        """
        for item_id in item_ids:
            await self.test_delete_item(item_id)

    async def verify_deleted_item(self, item_id):
        """Verifica que el item con el ID indicado ha sido eliminado.

        Se espera que la petición GET a /items/{id} retorne un status 404.
        Registra el proceso con iconos 🚀 y ✅.
        """
        headers = {"Authorization": f"Bearer {self.TOKEN}"}
        self.logger.info(f"🚀 Confirmando eliminación del item con ID: {item_id}")
        response = requests.get(f"{self.API_URL}/items/{item_id}", headers=headers)
        assert (
            response.status_code == 404
        ), f"❌ El item aún existe: status code {response.status_code}"
        self.logger.info(f"✅ Item con ID {item_id} confirmado eliminado.")
