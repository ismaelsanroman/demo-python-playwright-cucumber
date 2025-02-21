# features/steps/api_test_step.py
"""Módulo que define los steps para la funcionalidad de API_TEST en BDD."""

import asyncio

from behave import step

from features.pages.api_test_page import ApiTest


@step('I launch a login request and we get the token')
def step_send_login_request(context):
    """Ejecuta el login y almacena el token en context.token."""
    page = ApiTest()
    asyncio.run(page.test_login())
    context.token = page.TOKEN


@step('I launch the request to obtain all items')
def step_send_items_request(context):
    """Ejecuta la petición para obtener los ítems y guarda la lista en context."""
    page = ApiTest(context)
    asyncio.run(page.test_get_items())
    context.items_request = page.items_request


@step('I verify that all items are retrieved')
def step_verify_items_request(context):
    """Verifica que la lista de ítems cumpla con los criterios de la tabla."""
    page = ApiTest(context)
    data_table = [row.as_dict() for row in context.table]
    asyncio.run(page.verify_items_request(data_table))


@step('I send a creation request with the following parameters')
def step_send_creation_request(context):
    """Envía la petición para cada ítem de la tabla.

    - Guarda la última respuesta en context.creation_response.
    - Guarda los IDs de los ítems creados en context.created_item_ids.
    """
    page = ApiTest(context)
    data_table = [row.as_dict() for row in context.table]
    created_ids = []

    for params in data_table:
        creation_response = asyncio.run(page.test_create_item_from_params(params))
        context.creation_response = creation_response

        if creation_response.status_code == 201:
            created_ids.append(params["id"])
        else:
            context.failing_params = params
            context.duplicate_params = params

    context.created_item_ids = created_ids


@step('I confirm that the item has been "created" correctly')
def step_confirm_creation(context):
    """Verifica mediante GET que cada ítem se haya creado correctamente."""
    page = ApiTest(context)
    for item_id in context.created_item_ids:
        asyncio.run(page.verify_created_item(item_id))


@step('I delete the created elements')
def step_delete_created_items(context):
    """Elimina los ítems creados usando los IDs de context.created_item_ids."""
    page = ApiTest(context)
    asyncio.run(page.delete_created_items(context.created_item_ids))


@step('I confirm that the item has been "deleted" correctly')
def step_confirm_deletion(context):
    """Verifica que cada ítem eliminado ya no exista."""
    page = ApiTest(context)
    for item_id in context.created_item_ids:
        asyncio.run(page.verify_deleted_item(item_id))


@step('I verify that the item creation fails with an error message')
def step_verify_failed_creation(context):
    """Verifica que la creación del ítem haya fallado.

    Se asume que la última creación fallida se almacenó en
    context.creation_response.
    """
    page = ApiTest(context)
    asyncio.run(page.verify_failed_item_creation(context.creation_response))


@step('An item with ID {item_id:d} already exists')
def step_item_already_exists(context, item_id):
    """Asegura que exista un ítem con el ID indicado o lo crea si no existe."""
    page = ApiTest(context)
    asyncio.run(page.ensure_item_exists(item_id))


@step('I verify that the item creation fails due to duplicate ID')
def step_verify_duplicate_creation(context):
    """Verifica que crear un ítem con ID duplicado falle.

    Se asume que la última creación fallida está en
    context.creation_response.
    """
    page = ApiTest(context)
    asyncio.run(page.verify_duplicate_item_creation(context.creation_response))


@step('I launch the request to obtain an item with ID {item_id:d}')
def step_get_item_by_id(context, item_id):
    """Envía GET para obtener el ítem con el ID especificado y almacena la respuesta."""
    page = ApiTest(context)
    context.get_item_response = asyncio.run(page.get_item_by_id(item_id))


@step('I verify that the response indicates "Item not found"')
def step_verify_item_not_found(context):
    """Verifica que la respuesta indique que el ítem no existe."""
    page = ApiTest(context)
    asyncio.run(page.verify_item_not_found_response(context.get_item_response))


@step('I launch the request to obtain all items without a token')
def step_send_items_request_no_token(context):
    """Envía la petición para obtener ítems sin token y la almacena."""
    page = ApiTest(context)
    asyncio.run(page.test_get_items_no_token())
    context.items_request = page.items_request


@step('I verify that the response returns an error for a missing or invalid token')
def step_verify_missing_token_error(context):
    """Verifica la respuesta de la petición sin token."""
    page = ApiTest(context)
    asyncio.run(page.verify_missing_token_error(page.items_request))