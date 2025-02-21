# features/steps/api_test_step.py
"""Módulo que define los steps para la funcionalidad de API_TEST en BDD."""

import asyncio

from behave import step

from features.pages.api_test_page import ApiTest


@step('I launch a login request and we get the token')
def step_send_login_request(context):
    """Ejecuta login y almacena el token en context.token."""
    page = ApiTest()
    asyncio.run(page.test_login())
    context.token = page.TOKEN


@step('I launch the petition to obtain all the items')
def step_send_items_request(context):
    """Ejecuta la petición para obtener items y guarda la lista en context."""
    page = ApiTest(context)
    asyncio.run(page.test_get_items())
    context.items_request = page.items_request


@step('I verify that all items are obtained')
def step_verify_items_request(context):
    """Verifica que la lista de items cumpla con los criterios de la tabla."""
    page = ApiTest(context)
    data_table = [row.as_dict() for row in context.table]
    asyncio.run(page.verify_items_request(data_table))


@step('I send a creation request with the following parameters')
def step_send_creation_request(context):
    """Envía creación para cada item de la tabla y guarda sus IDs en context."""
    page = ApiTest(context)
    data_table = [row.as_dict() for row in context.table]
    created_ids = []
    for params in data_table:
        asyncio.run(page.test_create_item_from_params(params))
        created_ids.append(params["id"])
    context.created_item_ids = created_ids


@step('I confirm that the parameter has been "created" correctly')
def step_confirm_creation(context):
    """Verifica que cada item creado se ha creado correctamente."""
    page = ApiTest(context)
    for item_id in context.created_item_ids:
        asyncio.run(page.verify_created_item(item_id))


@step('I delete the created element(s)')
def step_delete_created_items(context):
    """Elimina los items creados usando los IDs en context.created_item_ids."""
    page = ApiTest(context)
    asyncio.run(page.delete_created_items(context.created_item_ids))


@step('I confirm that the parameter has been "deleted" correctly')
def step_confirm_deletion(context):
    """Verifica que cada item eliminado ya no existe."""
    page = ApiTest(context)
    for item_id in context.created_item_ids:
        asyncio.run(page.verify_deleted_item(item_id))
