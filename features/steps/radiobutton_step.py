# features\steps\checkbox_steps.py
"""Módulo que define los steps para la funcionalidad de RadioButton en BDD."""

from behave import step

from features.pages.radiobutton_page import RadioButton


@step('I select the "{radiobtn_name}" radio button')
def step_click_radiobutton(context, radiobtn_name: str):
    """Selecciona un Radio Button con el nombre proporcionado."""
    page = RadioButton(context.page)
    context.loop.run_until_complete(page.click_radio_button(radiobtn_name))


@step('I verify that radioButton "{radiobtn_name}" is selected')
def step_radiobutton_verify(context, radiobtn_name: str):
    """Verifica la selección un Radio Button con el nombre proporcionado."""
    page = RadioButton(context.page)
    context.loop.run_until_complete(page.verify_radio_button(radiobtn_name))


@step('I verify that the "{radiobtn_name}" radio button is disabled')
def step_radiobutton_disabled(context, radiobtn_name: str):
    """Verifica un Radio Button DESACTIVADO con el nombre proporcionado."""
    page = RadioButton(context.page)
    context.loop.run_until_complete(page.verify_radio_button_disabled(radiobtn_name))


@step('I verify that "{radiobtn_name}" is not selected')
def step_radiobutton_notSelected(context, radiobtn_name: str):
    """Verifica que no se seleccione un Radio Button con el nombre proporcionado."""
    page = RadioButton(context.page)
    context.loop.run_until_complete(page.verify_radiobutton_notSelected(radiobtn_name))
