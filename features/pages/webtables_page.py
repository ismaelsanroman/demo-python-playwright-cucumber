# features\pages\webtables_page.py
"""Módulo contiene la clase `TextBoxPage` para interacción con formularios de texto."""

from utils.error_dictionary import ErrorDictionary

from .base_page import BasePage

errors = ErrorDictionary()


class WebTables(BasePage):
    """Clase que representa la página de formulario de texto.

    Contiene localizadores y métodos para interactuar con los campos de entrada
    y el botón de añadir.
    """

    # LOCATORS
    # Button
    add_btn = "addNewRecordButton"
    search_box_input = "searchBox"
    select_rows_page_btn = "//select[@aria-label='rows per page']"
    num_page_input = '//input[@aria-label="jump to page"]'
    option_value = '//option[@value="5"]'
    all_rows = '//div[@class="rt-tr-group"]'

    async def get_table_data(self):
        """Obtiene los datos de la tabla como una lista de diccionarios."""
        table_locator = self.page.locator(".rt-table")
        rows = await table_locator.locator(".rt-tr-group").all()

        table_data = []
        for row in rows:
            cells = await row.locator(".rt-td").all_inner_texts()

            if len(cells) >= 6 and any(cells):
                table_data.append(
                    {
                        "First Name": cells[0].strip(),
                        "Last Name": cells[1].strip(),
                        "Age": cells[2].strip(),
                        "Email": cells[3].strip(),
                        "Salary": cells[4].strip(),
                        "Department": cells[5].strip(),
                    }
                )

        return table_data
