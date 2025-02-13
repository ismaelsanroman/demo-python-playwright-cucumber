# features/steps/base_step.py
"""Módulo que define los steps para la funcionalidad de TextBox en BDD."""

from behave import step
from pages.base_page import BasePage
from pages.elements_page import ElementsPage

from utils.error_dictionary import ErrorDictionary

errors = ErrorDictionary()


@step('I navigate to DemoQA and "{element}" Page')
def step_navigate_to_elements(context, element: str):
    """Navega a la página base de DemoQA y hace clic en el elemento especificado.

    Args:
        context (behave.runner.Context): Contexto de Behave con la config.
        element (str): Nombre del elemento a seleccionar, ej. 'Elements'.
    """
    base_url = context.config.userdata.get("base_url")
    base_page = BasePage(context.page)
    context.loop.run_until_complete(base_page.navigate(base_url))
    context.loop.run_until_complete(base_page.scroll_page(500))
    context.loop.run_until_complete(
        base_page.click_element(f"//h5[contains(.,'{element}')]")  # noqa: E231
    )


@step('I open the "{section}" section')
def step_open_text_box(context, section: str):
    """Abre la sección específica dentro de la página de elementos.

    Args:
        context (behave.runner.Context): Contexto de Behave.
        section (str): Nombre de la sección a abrir, ej. 'Text Box'.
    """
    elements_page = ElementsPage(context.page)
    context.loop.run_until_complete(elements_page.open_section_form(section))
