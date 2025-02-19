# features\steps\webtables_step.py
"""Módulo que define los steps para la funcionalidad de TextBox en BDD."""

from behave import step

from features.pages.webtables_page import WebTables


@step("I verify the table contains the following rows")
def verify_table_contains_rows(context):
    """Verifica que la tabla contenga los datos esperados."""
    page = WebTables(context.page)

    # Extraer los datos esperados desde la tabla de Behave
    expected_rows = [
        {
            "First Name": row["First Name"],
            "Last Name": row["Last Name"],
            "Age": row["Age"],
            "Email": row["Email"],
            "Salary": row["Salary"],
            "Department": row["Department"],
        }
        for row in context.table
    ]

    actual_rows = context.loop.run_until_complete(page.get_table_data())

    # Verificar que cada fila esperada exista en los datos reales
    missing_rows = [row for row in expected_rows if row not in actual_rows]

    assert not missing_rows, f"❌ These rows were not found in the table: {missing_rows}" # noqa
