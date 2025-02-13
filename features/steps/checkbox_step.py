# features/steps/checkbox_step.py
"""Módulo que define los steps para la funcionalidad de CheckBox en BDD."""


from behave import step

from features.pages.checkbox_page import CheckBoxPage


@step('I select the checkbox for "{checkbox_name}"')
def step_select_checkbox_for(context, checkbox_name):
    """Selecciona el checkbox con el nombre proporcionado."""
    page = CheckBoxPage(context.page)
    context.loop.run_until_complete(page.click_checkbox(checkbox_name))


@step("I verify that labels are selected")
def step_labels_selected(context):
    """Verifica que las etiquetas en la tabla Gherkin están seleccionadas."""
    page = CheckBoxPage(context.page)
    labels = [row["label"] for row in context.table]
    context.loop.run_until_complete(page.verify_labels_selected(labels, "selected"))


@step("I verify that labels are not selected")
def step_labels_not_selected(context):
    """Verifica que las etiquetas en la tabla Gherkin NO están seleccionadas."""
    page = CheckBoxPage(context.page)
    labels = [row["label"] for row in context.table]
    context.loop.run_until_complete(page.verify_labels_selected(labels, "not selected"))


@step('I deselect the checkbox for "{checkbox_name}"')
def step_deselect_checkbox_for(context, checkbox_name):
    """Deselecciona el checkbox con el nombre proporcionado, si está seleccionado."""
    page = CheckBoxPage(context.page)
    context.loop.run_until_complete(page.deselect_checkbox(checkbox_name))
