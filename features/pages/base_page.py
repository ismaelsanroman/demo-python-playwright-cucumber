# features/pages/base_page.py
from utils.logger import Logger

class BasePage:
    """
    Esta clase base requiere una `page` asíncrona de Playwright
    para ejecutar sus métodos.
    """
    def __init__(self, page):
        self.logger = Logger().get_logger()
        self.page = page  # page asíncrona

    async def navigate(self, url: str):
        self.logger.info(f"🌐 Navigating to: {url}")
        await self.page.goto(url)

    async def click_element(self, locator: str):
        self.logger.info(f"🖱  Clicking on element: {locator}")
        await self.page.locator(locator).scroll_into_view_if_needed()
        await self.page.locator(locator).focus()
        await self.page.click(locator)
        
    async def fill_element(self, locator: str, text: str):
        self.logger.info(f"⌨️ Filling element {locator} with text: {text}")
        await self.page.fill(locator, text)

    async def get_text(self, locator: str) -> str:
        text = await self.page.inner_text(locator)
        await self.page.locator(locator).scroll_into_view_if_needed()
        await self.page.locator(locator).focus()
        self.logger.info(f"🔍 Text from {locator}: {text}")
        return text

    async def find_element(self, selector: str, timeout: int = 5000):
        self.logger.info(f"🔍 Buscando elemento: {selector}")

        try:
            element = self.page.locator(selector)
            await element.wait_for(state="visible", timeout=timeout)
            self.logger.info(f"✅ Elemento encontrado: {selector}")
            return element
        except Exception as e:
            self.logger.error(f"❌ No se pudo encontrar el elemento {selector} dentro del tiempo de espera: {e}")
            return None