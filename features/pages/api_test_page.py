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
    """Clase para pruebas contra la API simulada."""

    def __init__(self, context=None):
        """Inicializa la configuración de la API y carga valores del contexto."""
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
        """Realiza la petición POST a /login para obtener el token."""
        response = requests.post(f"{self.API_URL}/login", json={})
        msg_login = f"❌ Error al hacer login: status {response.status_code}"
        assert response.status_code == 200, msg_login

        json_data = response.json()
        assert json_data["success"] is True, "❌ La respuesta de login no indicó éxito."
        token_ok = "❌ No se encontró 'token' en la respuesta de login."
        assert "token" in json_data, token_ok

        self.TOKEN = json_data["token"]
        self.logger.info(f"🔑 Token obtenido: {self.TOKEN}")

    async def test_get_items(self):
        """Realiza la petición GET a /items con el token."""
        headers = {"Authorization": f"Bearer {self.TOKEN}"}
        response = requests.get(f"{self.API_URL}/items", headers=headers)
        msg_items = f"❌ Error al obtener ítems: status {response.status_code}"
        assert response.status_code == 200, msg_items

        json_data = response.json()
        error_msg = "❌ La respuesta de /items no indicó éxito."
        assert json_data["success"] is True, error_msg
        is_list = isinstance(json_data["data"], list)
        assert is_list, "❌ 'data' no es una lista."

        self.items_request = json_data["data"]
        self.logger.info("📄 Se han obtenido todos los ítems.")
        first_items = json_data['data'][:3]
        self.logger.info(f"📄 Items (primeros 3): {first_items}...")

    async def test_get_items_no_token(self):
        """Realiza la petición GET a /items sin token."""
        self.logger.info("🚀 Enviando GET a /items sin token.")
        response = requests.get(f"{self.API_URL}/items")
        self.items_request = response
        msg = f"✅ Respuesta sin token: {response.status_code} - {response.text}"
        self.logger.info(msg)

    async def verify_items_request(self, data_table):
        """Verifica que la lista de ítems cumpla con los criterios especificados.

        Si no se han obtenido ítems, se lanza un ValueError.
        Se revisan campos como description, price, stock, available y
        cualquier otro, comparando valores directos o usando >, <, etc.
        """
        if self.items_request is None:
            raise ValueError(
                "No se han obtenido ítems. Llama primero a test_get_items()."
            )

        for criteria in data_table:
            matching_items = []
            for item in self.items_request:
                match = True
                for key, value in criteria.items():
                    val = value.strip()
                    if val:
                        item_value = item.get(key)
                        if item_value is None:
                            match = False
                            break
                        if key == "description":
                            if val not in str(item_value):
                                match = False
                                break
                        elif key in ["price", "stock"]:
                            if val.startswith(">") or val.startswith("<"):
                                operator = val[0]
                                try:
                                    threshold = float(val[1:])
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
                                    if float(item_value) != float(val):
                                        match = False
                                        break
                                except ValueError:
                                    match = False
                                    break
                        elif key == "available":
                            if str(item_value).lower() != val.lower():
                                match = False
                                break
                        else:
                            if str(item_value) != val:
                                match = False
                                break
                if match:
                    matching_items.append(item)

            msg_criteria = f"❌ No se encontró ningún ítem que cumpla {criteria}"
            assert matching_items, msg_criteria
            self.logger.info(f"📥 Criterios {criteria} -> Ítems: {matching_items}")

        self.logger.info("✅ Todos los criterios se han verificado correctamente.")

    async def test_create_item_from_params(self, params: dict):
        """Envía una petición POST a /items con los parámetros dados.

        No forzamos el assert == 201, pues en casos 'unhappy' puede ser 400/409.
        Devolvemos la respuesta para que se valide en el step correspondiente.
        """
        headers = {
            "Authorization": f"Bearer {self.TOKEN}",
            "Content-Type": "application/json",
        }
        try:
            if params["id"].strip():
                params["id"] = int(params["id"])
            else:
                params.pop("id")
        except KeyError:
            pass

        try:
            if "price" in params and params["price"].strip():
                params["price"] = float(params["price"])
            else:
                params.pop("price", None)
        except KeyError:
            pass

        try:
            if "stock" in params and params["stock"].strip():
                params["stock"] = int(params["stock"])
            else:
                params.pop("stock", None)
        except KeyError:
            pass

        try:
            if "available" in params and params["available"].strip():
                val = params["available"].lower()
                params["available"] = val == "true"
            else:
                params.pop("available", None)
        except KeyError:
            pass

        msg_params = f"🚀 Creando ítem con parámetros: {params}"
        self.logger.info(msg_params)
        response = requests.post(f"{self.API_URL}/items", json=params, headers=headers)
        msg_create = f"→ Respuesta creación: {response.status_code} - {response.text}"
        self.logger.info(msg_create)
        return response

    async def verify_created_item(self, item_id):
        """Verifica, vía GET /items/{item_id}, que el ítem exista."""
        headers = {"Authorization": f"Bearer {self.TOKEN}"}
        self.logger.info(f"🚀 Verificando ítem con ID {item_id}")
        response = requests.get(f"{self.API_URL}/items/{item_id}", headers=headers)
        msg_item = f"❌ Error al obtener el ítem creado: status {response.status_code}"
        assert response.status_code == 200, msg_item

        json_data = response.json()
        err_json = f"❌ Error al obtener el ítem: {json_data}"
        assert json_data["success"] is True, err_json
        self.logger.info(f"✅ Ítem verificado: {json_data['data']}")

    async def test_delete_item(self, item_id: int):
        """Envía una petición DELETE a /items/{item_id} para eliminarlo."""
        headers = {"Authorization": f"Bearer {self.TOKEN}"}
        msg_del = f"🚀 Enviando DELETE para el ítem con ID {item_id}"
        self.logger.info(msg_del)
        response = requests.delete(f"{self.API_URL}/items/{item_id}", headers=headers)
        del_err = f"❌ Error al borrar el ítem: status {response.status_code}"
        assert response.status_code == 200, del_err

        json_data = response.json()
        del_fail = f"❌ Falló la eliminación: {json_data}"
        assert json_data["success"] is True, del_fail
        msg_unexp = "❌ Mensaje de eliminación inesperado."
        assert json_data["message"] == "Item deleted", msg_unexp
        msg_ok = f"✅ Ítem con ID {item_id} eliminado correctamente."
        self.logger.info(msg_ok)

    async def delete_created_items(self, item_ids):
        """Envía DELETE para cada ítem en item_ids."""
        for item_id in item_ids:
            await self.test_delete_item(item_id)

    async def verify_deleted_item(self, item_id):
        """Verifica que el ítem con ID item_id ya no exista.

        GET /items/{item_id} debe retornar 404 si fue borrado.
        """
        headers = {"Authorization": f"Bearer {self.TOKEN}"}
        self.logger.info(f"🚀 Confirmando la eliminación del ítem con ID {item_id}")
        response = requests.get(f"{self.API_URL}/items/{item_id}", headers=headers)
        msg_err = f"❌ El ítem todavía existe (status {response.status_code})"
        assert response.status_code == 404, msg_err
        self.logger.info(f"✅ Ítem con ID {item_id} confirmado como eliminado.")

    async def verify_failed_item_creation(self, creation_response):
        """Verifica la creación haya fallado con código 4xx y un mensaje de error."""
        status = creation_response.status_code
        msg_stat = f"❌ Se esperaba un error (400 o 409), pero se obtuvo {status}."
        self.logger.info(f"→ Verificando creación fallida: {status}")
        assert status in (400, 409), msg_stat

        json_data = creation_response.json()
        ok_fail = "❌ La creación fallida se marcó como exitosa."
        assert not json_data.get("success", True), ok_fail
        msg_key = "❌ No se encontró 'message' en la respuesta."
        assert "message" in json_data, msg_key
        err_str = f"✅ Creación fallida verificada con mensaje: {json_data['message']}"
        self.logger.info(err_str)

    async def ensure_item_exists(self, item_id: int):
        """Asegura que exista un ítem con el ID dado.

        Si no existe, lo crea con valores por defecto.
        """
        headers = {"Authorization": f"Bearer {self.TOKEN}"}
        msg_ver = f"🚀 Verificando existencia del ítem con ID {item_id}"
        self.logger.info(msg_ver)
        response = requests.get(f"{self.API_URL}/items/{item_id}", headers=headers)

        if response.status_code == 200:
            msg_has = f"✅ El ítem con ID {item_id} ya existe."
            self.logger.info(msg_has)
            return

        default_item = {
            "id": item_id,
            "name": f"Item {item_id}",
            "description": "Default description",
            "category": "Default",
            "price": 10.0,
            "stock": 5,
            "available": True,
        }
        msg_cre = f"🚀 Creando ítem con ID {item_id} porque no existía."
        self.logger.info(msg_cre)
        resp = requests.post(
            f"{self.API_URL}/items", json=default_item, headers=headers
        )  # noqa
        assert resp.status_code == 201, f"❌ Error al crear el ítem con ID {item_id}."

    async def verify_duplicate_item_creation(self, creation_response):
        """Verifica que crear un ítem con ID duplicado falle con status 409."""
        status = creation_response.status_code
        msg_dup = f"❌ Se esperaba error 409, pero se obtuvo {status}."
        self.logger.info(f"→ Verificando error de ítem duplicado: {status}")
        assert status == 409, msg_dup

        json_data = creation_response.json()
        dup_fail = "❌ Se marcó como exitosa la creación con ID duplicado."
        assert not json_data.get("success", True), dup_fail
        conf_msg = f"✅ Error de ID duplicado confirmado: {json_data.get('message')}"
        self.logger.info(conf_msg)

    async def get_item_by_id(self, item_id: int):
        """Realiza GET /items/{item_id} y retorna la respuesta."""
        headers = {"Authorization": f"Bearer {self.TOKEN}"}
        self.logger.info(f"🚀 Obteniendo ítem con ID {item_id}")
        return requests.get(f"{self.API_URL}/items/{item_id}", headers=headers)

    async def verify_item_not_found_response(self, response):
        """Verifica que la respuesta indique un 404 y 'Item not found'."""
        msg_404 = f"❌ Se esperaba 404, pero se obtuvo {response.status_code}."
        assert response.status_code == 404, msg_404

        json_data = response.json()
        not_found = "❌ No se encontró el mensaje 'Item not found'."
        assert "Item not found" in json_data.get("message", ""), not_found
        self.logger.info("✅ La respuesta indica correctamente 'Item not found'.")

    async def verify_missing_token_error(self, response):
        """Verifica que la petición sin token retorne 401 y un mensaje apropiado."""
        status = response.status_code
        self.logger.info(f"→ Verificando error por token faltante: {status}")
        msg_401 = f"❌ Se esperaba 401, pero se obtuvo {status}."
        assert status == 401, msg_401

        json_data = response.json()
        message = json_data.get("message", "")
        cond = ("autorizac" in message.lower()) or ("token" in message.lower())
        err_tkn = f"❌ El mensaje '{message}' no menciona 'token' ni 'autorización'."
        assert cond, err_tkn
        self.logger.info("✅ Error por token faltante o inválido verificado.")