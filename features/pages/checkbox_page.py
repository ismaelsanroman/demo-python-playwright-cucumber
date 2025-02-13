# features/pages/checkbox_page.py
"""Módulo que define los steps para la funcionalidad de CheckBox en BDD."""

from .base_page import BasePage


class CheckBoxPage(BasePage):
    """Clase para interactuar con los checkboxes en la UI."""

    # LOCATORS
    All_verify_label = "#result"
    expand_button = "Expand all"
    collapse_button = "Collapse all"

    async def click_checkbox(self, locator: str):
        """Expande y selecciona un checkbox con el texto proporcionado."""
        self.logger.info(f"🖱️ Haciendo clic en el checkbox: {locator}")
        await self.click_button(self.expand_button)
        await self.page.locator("label").filter(has_text=locator).click()

    async def is_checkbox_selected(self, locator: str) -> bool:
        """Verifica si checkbox está seleccionado comparando texto en el resultado."""
        element = self.page.locator(self.All_verify_label)
        is_element_present = await element.count() > 0

        if not is_element_present:
            self.logger.info(
                "⚠️ No se encontró el contenedor de selección. "
                f"El checkbox '{locator}' NO está seleccionado."
            )
            return False

        selected_text = await element.text_content()
        if selected_text is None:
            self.logger.info(
                "⚠️ El contenedor de selección está vacío. "
                f"El checkbox '{locator}' NO está seleccionado."
            )
            return False

        is_selected = locator.lower() in selected_text.lower()
        self.logger.info(
            "✅ Estado del checkbox '{locator}': "
            f"{'Seleccionado' if is_selected else 'No seleccionado'}"
        )
        return is_selected

    async def deselect_checkbox(self, locator: str):
        """Si un checkbox está seleccionado, deselecciona y espera a que desaparezca."""
        is_selected = await self.is_checkbox_selected(locator)
        if is_selected:
            self.logger.info(f"🔄 Deseleccionando el checkbox: {locator}")
            await self.click_checkbox(locator)
            await self.page.wait_for_timeout(500)
        else:
            self.logger.info(
                "✅ El checkbox '{locator}' ya está deseleccionado. "
                "No es necesario hacer clic."
            )

    async def verify_checkbox_clicked(self, locator: str, clicked: bool = True):
        """Verifica que un checkbox esté o no seleccionado."""
        is_selected = await self.is_checkbox_selected(locator)

        if clicked and not is_selected:
            self.logger.error(
                "🪲 ERROR: El checkbox '{locator}' debería estar "
                "seleccionado, pero NO lo está."
            )
            raise AssertionError(
                f'🪲 Error: El checkbox "{locator}" NO está seleccionado.'
            )

        if not clicked and is_selected:
            self.logger.error(
                "🪲 ERROR: El checkbox '{locator}' debería estar "
                "deseleccionado, pero SIGUE presente."
            )
            raise AssertionError(
                f'🪲 Error: El checkbox "{locator}" debería estar '
                "deseleccionado, pero aún aparece en la selección."
            )

        self.logger.info(
            "✅ Verificación exitosa: El checkbox '{locator}' está "
            f"{'seleccionado' if clicked else 'deseleccionado'}."
        )

    async def verify_labels_selected(self, expected_labels: list, state: str):
        """Verifica que las etiquetas esperadas estén o no seleccionadas."""
        element = self.page.locator(self.All_verify_label)
        is_element_present = await element.count() > 0
        state = state.lower()

        if state == "selected":
            if not is_element_present:
                self.logger.error(
                    "🪲 ERROR: No se encontró el contenedor de etiquetas "
                    "seleccionadas."
                )
                raise AssertionError(
                    "🪲 Error: No se encontró el contenedor de etiquetas "
                    "seleccionadas."
                )

            selected_text = await element.text_content()
            if not selected_text:
                self.logger.error(
                    "🪲 ERROR: El contenedor de etiquetas seleccionadas " "está vacío."
                )
                raise AssertionError(
                    "🪲 Error: El contenedor de etiquetas seleccionadas " "está vacío."
                )

            missing_labels = [
                label
                for label in expected_labels
                if label.lower() not in selected_text.lower()
            ]
            if missing_labels:
                self.logger.error(
                    "🪲 ERROR: Algunas etiquetas no están seleccionadas. "
                    f"Faltan: {', '.join(missing_labels)}."
                )
                raise AssertionError(
                    "🪲 Error: Algunas etiquetas no están seleccionadas. "
                    f'Faltan: {", ".join(missing_labels)}. '
                    f"Texto encontrado: {selected_text}"
                )

            self.logger.info(
                "✅ Todas las etiquetas esperadas están seleccionadas: "
                f"{expected_labels}"
            )

        elif state == "not selected":
            # Esperar antes de verificar para evitar falsos negativos
            await self.page.wait_for_timeout(500)
            if is_element_present:
                self.logger.error(
                    "🪲 ERROR: Se encontró el contenedor "
                    f"'{self.All_verify_label}' en la página, "
                    "pero NO debería estar presente."
                )
                raise AssertionError(
                    f'🪲 Error: Se encontró el contenedor "{self.All_verify_label}" '
                    "en la página, pero NO debería estar presente."
                )

            self.logger.info(
                "✅ Verificación exitosa: No hay etiquetas seleccionadas en "
                "la página."
            )

        else:
            self.logger.error(
                "🪲 ERROR: Estado '{state}' no reconocido. "
                "Use 'selected' o 'not selected'."
            )
            raise ValueError(
                "🪲 Error: Estado '{state}' no reconocido. "
                "Use 'selected' o 'not selected'."
            )
