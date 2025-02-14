# features\pages\radiobutton_page.py
"""Módulo que define los steps para la funcionalidad de RadioButton en BDD."""

from utils.error_dictionary import ErrorDictionary

from .base_page import BasePage

errors = ErrorDictionary()


class RadioButton(BasePage):
    """Clase para interactuar con checkboxes en la UI."""

    # LOCATORS
    # Labels verify
    msg_verify = "//p[@class='mt-3']"

    async def click_radio_button(self, locator: str):
        """Clica en un botón de radio y verifica si se ha seleccionado correctamente."""
        radiobtn_label = self.page.locator("label").filter(has_text=locator)
        radiobtn_input = self.page.get_by_role("radio", name=locator)

        try:
            await radiobtn_label.click()

            if not await radiobtn_input.is_checked():
                msg = f"🪲 Error: No se ha seleccionado el botón '{locator}'"
                self.logger.error(msg)
                raise AssertionError(msg)

        except Exception as e:
            msg = f"🪲 No se ha seleccionado el botón '{locator}' debido a: {str(e)}"
            self.logger.error(msg)
            raise AssertionError(msg)

    async def verify_radiobutton_notSelected(self, locator: str):
        """Verifica que no está seleccionado."""
        radiobtn = self.page.get_by_text(locator)

        if await radiobtn.is_checked():
            msg = f"🪲 Error: botón '{locator}' seleccionado"
            self.logger.error(msg)
            raise AssertionError(msg)

    async def verify_radio_button(self, locator: str):
        """Comprueba que el mensahe de selección coincida con el localizador."""
        msg_verify = self.page.get_by_role("paragraph").get_by_text(locator)
        is_element_present = await msg_verify.count() > 0
        if not is_element_present:
            msg = f"🪲 ERROR: No se ha seleccionado el radioButton {locator}."
            self.logger.error(msg)
            raise AssertionError(msg)

    async def verify_radio_button_disabled(self, locator: str):
        """Verifica que no está activo ni se puede seleccionar."""
        radiobtn = self.page.get_by_text(locator)
        if await radiobtn.is_disabled():
            self.logger.info(f"✅ El botón de radio '{locator}' está deshabilitado.")

            try:
                await radiobtn.click(timeout=100)
                msg = f"🪲 Error: Se pudo hacer clic en el botón '{locator}'."
                self.logger.error(msg)
                raise AssertionError(msg)
            except Exception:
                self.logger.info(f"✅ No se pudo hacer clic en el botón '{locator}'.")

            return True

        self.logger.warning(f"⚠️ El botón de radio '{locator}' NO está deshabilitado.")
        return False
