# features/pages/elements_page.py
"""Módulo contiene clase `ElementsPage` para interactuar con la página de elementos."""

from .base_page import BasePage


class ElementsPage(BasePage):
    """Clase que representa la página de elementos.

    Proporciona métodos para interactuar con sus secciones específicas.
    """

    # Locators
    textBox_button = "text=Text Box"
    checkBox_button = "text=Radio Button"
    radioButton_button = "text=Web Tables"
    webTables_button = "text=Web Tables"
    buttons_button = "text=Buttons"
    links_button = "text=Links"
    brokenLinksImages_button = "text=Broken Links - Images"
    uploadAndDownload_button = "text=Upload and Download"
    dynamicProperties_button = "text=Dynamic Properties"

    async def open_section_form(self, section):
        """Abre una sección específica de la página de elementos.

        Args:
            section (str): Nombre de la sección a abrir.
        """
        await self.click_element(f"text={section}")
