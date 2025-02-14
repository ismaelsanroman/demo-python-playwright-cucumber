# features/pages/textbox_page.py
"""Módulo contiene la clase `TextBoxPage` para interacción con formularios de texto."""

from utils.error_dictionary import ErrorDictionary

from .base_page import BasePage

errors = ErrorDictionary()


class TextBoxPage(BasePage):
    """Clase que representa la página de formulario de texto.

    Contiene localizadores y métodos para interactuar con los campos de entrada
    y el botón de envío.
    """

    # LOCATORS
    # Labels
    full_name_label = "userName-label"
    email_label = "userEmail-label"
    current_address_label = "currentAddress-label"
    permanent_address_label = "permanentAddress-label"

    # Input fields
    full_name_input = "#userName"
    email_input = "#userEmail"
    email_error_input = "//input[contains(@class,'mr-sm-2 field-error form-control')]"
    current_address_input = "#currentAddress"
    permanent_address_input = "#permanentAddress"

    # Button
    submit_button = "#submit"

    # Labels request
    name_request = "#name"
    email_request = "#email"
    current_address_request = "//p[@id='currentAddress']"
    permanent_address_request = "//p[@id='permanentAddress']"

    async def fill_and_verify_form(
        self,
        name,
        email,
        current_address,
        permanent_address,
    ):
        """Completa el formulario con los datos proporcionados."""
        await self.fill_element(self.full_name_input, name)
        await self.fill_element(self.email_input, email)
        await self.fill_element(self.current_address_input, current_address)
        await self.fill_element(self.permanent_address_input, permanent_address)

    async def submit_form(self):
        """Hace clic en el botón de enviar formulario."""
        await self.click_element(self.submit_button)

    async def verify_submitted_data(
        self,
        expected_name,
        expected_email,
        expected_address,
        expected_permanent_address,
    ):
        """Verifica que los datos mostrados tras enviar el formulario coincidan.

        Confirma que cada texto en pantalla coincide con el valor esperado.
        """
        name_text = await self.get_text(self.name_request)
        email_text = await self.get_text(self.email_request)
        address_text = await self.get_text(self.current_address_request)
        permanent_address_text = await self.get_text(self.permanent_address_request)

        assert expected_name[:25] in f"Name:{name_text}", ( # noqa
            f"❌ Nombre incorrecto: esperado '{expected_name}', "
            f"obtenido '{name_text}'"
        )
        assert expected_email in f"Email:{email_text}", ( # noqa
            f"❌ Email incorrecto: esperado '{expected_email}', "
            f"obtenido '{email_text}'"
        )
        assert expected_address in f"Current Address :{address_text}", ( # noqa
            f"❌ Dirección incorrecta: esperado '{expected_address}', "
            f"obtenido '{address_text}'"
        )
        assert expected_permanent_address in (
            f"Permananet Address :{permanent_address_text}" # noqa
        ), (
            f"❌ Dirección permanente incorrecta: esperado "
            f"'{expected_permanent_address}', obtenido "
            f"'{permanent_address_text}'"
        )

        print("✅ Los datos mostrados coinciden con los ingresados.")

    async def error_email_submitted_data(self):
        """Busca y verifica si se muestra un error en el campo de email."""
        await self.find_element(self.email_error_input)
