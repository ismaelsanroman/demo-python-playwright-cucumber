# features/steps/api_test_step.py
"""Módulo que define los steps para la funcionalidad de API_TEST en BDD."""


import asyncio

from behave import step

from features.pages.api_test_page import ApiTest


@step("I launch a login request and we get the token")
def step_send_login_request(context):
    """Lanzamos la petición de login y guardamos el TOKEN."""
    page = ApiTest()
    asyncio.run(page.test_login())
    context.token = page.TOKEN


@step("I launch the petition to obtain all the items")
def step_send_items_request(context):
    """Lanzamos la petición para obtener todos los items."""
    page = ApiTest(context)
    asyncio.run(page.test_get_items())
    context.items_request = page.items_request


@step("I verify that all items are obtained")
def step_verify_items_request(context):
    """Verificamos que la lista de items contiene los criterios especificados."""
    page = ApiTest(context)
    data_table = [row.as_dict() for row in context.table]
    asyncio.run(page.verify_items_request(data_table))


@step("I send a creation request with the following parameters")
def step_(context):
    """."""
    page = ApiTest(context)
    data_table = [row.as_dict() for row in context.table]
    asyncio.run(page)


@step('I confirm that the parameter has been "{accion}" correctly')
def step_(context, accion):
    """."""
    page = ApiTest(context)
    asyncio.run(page)


@step("I delete the element created by its ID")
def step_(context):
    """."""
    page = ApiTest(context)
    asyncio.run(page)
