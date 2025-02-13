# features/pages/elements_page.py
"""Módulo contiene clase `ElementsPage` para interactuar con la página de elementos."""

from .base_page import BasePage


class ElementsPage(BasePage):
    """Clase que representa la página de elementos.

    Proporciona métodos para interactuar con sus secciones específicas.
    """

    async def open_section_form(self, section: str):
        """Abre una sección específica de la página de elementos.

        Args:
            section (str): Nombre de la sección a abrir.
        """
        self.logger.info(f"📂 Abriendo la sección: {section}")
        await self.click_element(f"text={section}")
        self.logger.info(f"✅ Sección '{section}' abierta correctamente.")
