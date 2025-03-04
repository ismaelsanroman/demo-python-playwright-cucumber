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
    form_validated = ".was-validated"

    # Button
    add_btn = "Add"
    submit_btn = "Submit"

    # Box
    search_box_input = "#searchBox"
    num_page_input = '//input[@aria-label="jump to page"]'
    option_value = '//option[@value="5"]'
    all_rows = '//div[@class="rt-tr-group"]'
    select_rows_page_btn = "//select[@aria-label='rows per page']"

    # Fill
    firstName_fill = "#firstName"
    lastName_fill = "#lastName"
    email_fill = "#userEmail"
    age_fill = "#age"
    salary_fill = "#salary"
    departament_fill = "#department"

    async def get_table_data(self):
        """Devuelve los datos visibles de la tabla en una lista de diccionarios."""
        self.logger.info("📋 Obteniendo datos de la tabla...")

        rows = await self.page.locator(".rt-tr-group").all()
        if not rows:
            self.logger.warning("⚠️ La tabla no contiene filas.")
            return []

        table_data = []
        for row in rows:
            cells = await row.locator(".rt-td").all_inner_texts()
            if len(cells) < 6:
                continue  # Omitimos filas incompletas

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

        self.logger.info(f"✅ {len(table_data)} filas obtenidas de la tabla.")
        return table_data

    async def click_add_entry(
        self,
        firstName: str,
        lastName: str,
        email: str,
        age: str,
        salary: str,
        departament: str,
    ):
        """Añade una nueva entrada a la tabla rellenando el formulario y enviándolo."""
        self.logger.info("📝 Añadiendo nueva entrada a la tabla.")

        if not await self.click_button(self.add_btn):
            self.logger.error("❌ Fallo al hacer clic en 'Add'.")
            return

        # Rellenar formulario
        await self.fill_element(self.firstName_fill, firstName)
        await self.fill_element(self.lastName_fill, lastName)
        await self.fill_element(self.email_fill, email)
        await self.fill_element(self.age_fill, age)
        await self.fill_element(self.salary_fill, salary)
        await self.fill_element(self.departament_fill, departament)

        # Enviar formulario
        if not await self.click_button(self.submit_btn):
            self.logger.error("❌ Fallo al hacer clic en 'Submit'.")
            return

        self.logger.info("✅ Entrada añadida con éxito.")

    async def form_class_validated(self):
        """Verifica si el formulario ha sido validado correctamente."""
        element = await self.find_element(self.form_validated)
        if element:
            self.logger.info("✅ Formulario validado correctamente.")
        else:
            self.logger.warning("⚠️ La validación del formulario no fue encontrada.")
        return element
