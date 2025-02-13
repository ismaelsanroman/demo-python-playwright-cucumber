# features/pages/base_page.py
"""Módulo que contiene la clase base `BasePage` para interacción con Playwright."""

from utils.logger import Logger


class BasePage:
    """Clase base para la interacción con la página usando Playwright."""

    def __init__(self, page):
        """Inicializa la clase BasePage con una instancia de `page` de Playwright.

        Args:
            page (playwright.async_api.Page): Instancia de la página en Playwright.
        """
        self.logger = Logger().get_logger()
        self.page = page  # page asíncrona

    async def navigate(self, url: str):
        """Navega a la URL especificada."""
        self.logger.info(f"🌐 Navigating to: {url}")
        await self.page.goto(url)

    async def click_element(self, locator: str):
        """Hace clic en un elemento identificado por el `locator`."""
        self.logger.info(f"🖱️  Clicking on element: {locator}")
        await self.page.locator(locator).scroll_into_view_if_needed()
        await self.page.locator(locator).focus()
        await self.page.click(locator)

    async def click_button(self, locator: str):
        """Hace clic en un botón identificado por el `locator`."""
        self.logger.info(f"🖱️  Clicking button: {locator}")
        await self.page.get_by_role("button", name=locator).click()

    async def fill_element(self, locator: str, text: str):
        """Rellena campo de entrada identificado por `locator` con el texto `text`."""
        self.logger.info(f"⌨️ Filling element {locator} with text: {text}")
        await self.page.fill(locator, text)

    async def get_text(self, locator: str) -> str:
        """Obtiene el texto de un elemento identificado por `locator`."""
        text = await self.page.inner_text(locator)
        await self.page.locator(locator).scroll_into_view_if_needed()
        await self.page.locator(locator).focus()
        self.logger.info(f"🔍 Text from {locator}: {text}")
        return text

    async def find_element(self, selector: str, timeout: int = 5000):
        """Busca un elemento en la página y espera hasta que sea visible.

        Args:
            selector (str): Selector del elemento a encontrar.
            timeout (int, opcional): Tiempo máximo de espera en milisegundos.
                Por defecto, 5000ms.

        Returns:
            playwright.async_api.Locator | None: El elemento encontrado o None
                si no se encuentra.
        """
        self.logger.info(f"🔍 Buscando elemento: {selector}")

        try:
            element = self.page.locator(selector)
            await element.wait_for(state="visible", timeout=timeout)
            self.logger.info(f"✅ Elemento encontrado: {selector}")
            return element
        except Exception as e:
            self.logger.error(
                "❌ No se pudo encontrar el elemento %s dentro del "
                "tiempo de espera: %s",
                selector,
                e,
            )
            return None

    async def scroll_page(self, pixeles: str):
        """Realizamos scroll de X pixeles en una página."""
        self.logger.info(f"📜 Scrolling page {pixeles} píxeles")
        await self.page.evaluate(f"window.scrollBy(0, {pixeles})")

    async def scroll_final_page(self):
        """Realizamos scroll al final de la página."""
        self.logger.info("📜 Scrolling final page")
        await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
