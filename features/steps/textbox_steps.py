# features/steps/textbox_steps.py
"""Módulo que define los steps para la funcionalidad de TextBox en BDD."""

from behave import given, then, when
from pages.base_page import BasePage
from pages.elements_page import ElementsPage
from pages.textbox_page import TextBoxPage

from utils.error_dictionary import ErrorDictionary

errors = ErrorDictionary()


@given('I navigate to DemoQA and "{element}" Page')
def step_navigate_to_elements(context, element: str):
    """Navega a la página base de DemoQA y hace clic en el elemento especificado.

    Args:
        context (behave.runner.Context): Contexto de Behave con la config.
        element (str): Nombre del elemento a seleccionar, ej. 'Elements'.
    """
    base_url = context.config.userdata.get("base_url")
    base_page = BasePage(context.page)
    context.loop.run_until_complete(base_page.navigate(base_url))
    context.loop.run_until_complete(
        base_page.click_element(f"//h5[contains(.,'{element}')]")
    )


@when('I open the "{section}" section')
def step_open_text_box(context, section: str):
    """Abre la sección específica dentro de la página de elementos.

    Args:
        context (behave.runner.Context): Contexto de Behave.
        section (str): Nombre de la sección a abrir, ej. 'Text Box'.
    """
    elements_page = ElementsPage(context.page)
    context.loop.run_until_complete(elements_page.open_section_form(section))


@then("I fill in the form with the following data")
def fill_in_and_send_form(context):
    """Completa y envía el formulario con la información proporcionada en la tabla.

    Args:
        context (behave.runner.Context): Contexto de Behave con una data table
            que incluye name, email, current_address y permanent_address.
    """
    textbox_page = TextBoxPage(context.page)
    data_table = [row.as_dict() for row in context.table]
    for row in data_table:
        name = row["name"]
        email = row["email"]
        current_address = row["current_address"]
        permanent_address = row["permanent_address"]

    context.loop.run_until_complete(
        textbox_page.fill_and_verify_form(
            name, email, current_address, permanent_address
        )
    )
    context.loop.run_until_complete(textbox_page.submit_form())


@then("I verify the form with the following data")
def verify_submitted_form(context):
    """Verifica que el formulario enviado muestre los datos indicados en la tabla.

    Args:
        context (behave.runner.Context): Contexto de Behave con la data table
            para comparar los datos del formulario.
    """
    textbox_page = TextBoxPage(context.page)
    data_table = [row.as_dict() for row in context.table]
    for row in data_table:
        name = row["name"]
        email = row["email"]
        current_address = row["current_address"]
        permanent_address = row["permanent_address"]

    context.loop.run_until_complete(
        textbox_page.verify_submitted_data(
            name, email, current_address, permanent_address
        )
    )


@then("I verify the form fails")
def verify_submitted_form_fail(context):
    """Verifica que el formulario muestre un error por email inválido.

    Args:
        context (behave.runner.Context): Contexto de Behave.
    """
    textbox_page = TextBoxPage(context.page)
    context.loop.run_until_complete(textbox_page.error_email_submitted_data())
