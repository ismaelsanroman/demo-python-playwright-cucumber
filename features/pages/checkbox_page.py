# features/pages/checkbox_page.py
"""Módulo que define los steps para la funcionalidad de CheckBox en BDD."""

import re

from utils.error_dictionary import ErrorDictionary

from .base_page import BasePage

errors = ErrorDictionary()


class CheckBoxPage(BasePage):
    """Clase para interactuar con checkboxes en la UI."""

    # LOCATORS
    All_verify_label = "#result"

    # Buttons
    expand_button = "Expand all"
    collapse_button = "Collapse all"

    # Expand sections button
    home_section_btn = {"name": "Toggle"}

    async def click_checkbox(self, locator: str):
        """Expande y selecciona un checkbox si existe."""
        self.logger.info(f"🖱️ Intentando seleccionar checkbox: {locator}")

        checkbox = self.page.locator("label").filter(has_text=locator)

        if await checkbox.count() == 0:
            self.logger.info(
                f"⚠️ Checkbox '{locator}' no encontrado. Intentando expandir..."
            )
            await self.click_button(self.expand_button)
            await checkbox.click()

            if await checkbox.count() == 0:
                self.logger.info(
                    f"❌ Checkbox '{locator}' no encontrado. Pasando al siguiente paso."
                )
                return

        await checkbox.click()

    async def is_checkbox_selected(self, locator: str) -> bool:
        """Verifica si un checkbox está seleccionado."""
        element = self.page.locator(self.All_verify_label)
        if await element.count() == 0:
            self.logger.info(f"⚠️ Checkbox '{locator}' no seleccionado.")
            return False

        selected_text = await element.text_content() or ""
        is_selected = locator.lower() in selected_text.lower()

        if is_selected:
            self.logger.info(f"✅ Checkbox '{locator}' seleccionado.")
        else:
            check = self.page.locator("label").filter(has_text=locator)
            exists = await check.count() > 0
            msg = "⚠️ Checkbox en la página pero no seleccionado."
            if not exists:
                msg = "❌ Checkbox no encontrado en la página."
            self.logger.info(f"{msg} '{locator}'")

        return is_selected

    async def deselect_checkbox(self, locator: str):
        """Si un checkbox está seleccionado, lo deselecciona."""
        if await self.is_checkbox_selected(locator):
            self.logger.info(f"🔄 Deseleccionando: {locator}")
            await self.click_checkbox(locator)
            if await self.is_checkbox_selected(locator):
                msg = f"🪲 ERROR: '{locator}' sigue seleccionado."
                self.logger.error(msg)
                raise AssertionError(msg)
            self.logger.info(f"✅ Checkbox '{locator}' deseleccionado.")
        else:
            self.logger.info(f"✅ Checkbox '{locator}' ya deseleccionado.")

    async def verify_checkbox_clicked(self, locator: str, clicked: bool = True):
        """Verifica el estado de un checkbox."""
        is_selected = await self.is_checkbox_selected(locator)
        if clicked and not is_selected:
            msg = f"🪲 ERROR: '{locator}' debería estar seleccionado."
            self.logger.error(msg)
            raise AssertionError(msg)
        if not clicked and is_selected:
            msg = f"🪲 ERROR: '{locator}' sigue seleccionado."
            self.logger.error(msg)
            raise AssertionError(msg)
        self.logger.info(f"✅ Checkbox '{locator}' verificado.")

    async def verify_labels_selected(self, expected_labels: list, state: str):
        """Verifica las etiquetas seleccionadas."""
        element = self.page.locator(self.All_verify_label)
        is_element_present = await element.count() > 0
        state = state.lower()

        if state == "selected":
            if not is_element_present:
                msg = "🪲 ERROR: No hay etiquetas seleccionadas."
                self.logger.error(msg)
                raise AssertionError(msg)

            selected_text = await element.text_content() or ""
            missing = [
                label
                for label in expected_labels
                if label.lower() not in selected_text.lower()
            ]
            if missing:
                msg = f"🪲 ERROR: Faltan etiquetas: {', '.join(missing)}."
                self.logger.error(msg)
                raise AssertionError(msg)
            self.logger.info(f"✅ Etiquetas seleccionadas: {expected_labels}")

        elif state == "not selected":
            await self.page.wait_for_timeout(500)
            if not is_element_present:
                self.logger.info("✅ No hay etiquetas seleccionadas.")
                return

            selected_text = await element.text_content() or ""
            still_selected = [
                label
                for label in expected_labels
                if label.lower() in selected_text.lower()
            ]
            if still_selected:
                msg = f"🪲 ERROR: Aún seleccionadas: {', '.join(still_selected)}."
                self.logger.error(msg)
                raise AssertionError(msg)
            self.logger.info(f"✅ Etiquetas deseleccionadas: {expected_labels}")

        else:
            msg = f"🪲 ERROR: Estado '{state}' inválido."
            self.logger.error(msg)
            raise ValueError(msg)

    async def expand_section(self, section: str):
        """Expande las secciones para visualizar o clicar."""
        self.logger.info(f"🗞️ Expandiendo la sección indicada: {section}")
        expandable_second = {"desktop", "documents", "downloads"}
        expandable_third = {"workspace", "office"}
        home_dropdown = self.page.get_by_role("button", **self.home_section_btn)

        if section.lower().strip() == "home":
            await home_dropdown.click()

        elif section.lower().strip() in expandable_second:
            await home_dropdown.click()
            item_locator = self.page.get_by_role("listitem").filter(
                has_text=re.compile(rf"^{section.capitalize()}$")
            )
            await item_locator.get_by_label("Toggle").click()

        elif section.lower().strip() in expandable_third:
            item_locator = self.page.get_by_role("listitem").filter(
                has_text=re.compile(rf"^{section.capitalize()}$")
            )
            await item_locator.get_by_label("Toggle").click()

        else:
            msg = f"🪲 ERROR: '{section} no es un desplegable válido."
            self.logger.error(msg)
            raise ValueError(msg)
