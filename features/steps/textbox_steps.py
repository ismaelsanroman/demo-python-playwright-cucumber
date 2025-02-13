# features/steps/textbox_steps.py
"""Módulo que define los steps para la funcionalidad de TextBox en BDD."""

from behave import step
from pages.textbox_page import TextBoxPage

from utils.error_dictionary import ErrorDictionary

errors = ErrorDictionary()


@step("I fill in the form with the following data")
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


@step("I verify the form with the following data")
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


@step("I verify the form fails")
def verify_submitted_form_fail(context):
    """Verifica que el formulario muestre un error por email inválido.

    Args:
        context (behave.runner.Context): Contexto de Behave.
    """
    textbox_page = TextBoxPage(context.page)
    context.loop.run_until_complete(textbox_page.error_email_submitted_data())
