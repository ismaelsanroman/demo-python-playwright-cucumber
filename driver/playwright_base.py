# driver/playwright_base.py
"""Módulo para gestionar el navegador utilizando Playwright."""

from playwright.sync_api import sync_playwright


class PlaywrightBase:
    """Clase base para gestionar el navegador con Playwright."""

    _playwright = None
    _browser = None
    _context = None
    _page = None

    @classmethod
    def start_browser(cls, headless=True, browser_type="chromium"):
        """Inicia el navegador y configura un contexto y una página nueva.

        Args:
            headless (bool, opcional): Ejecutar en modo 'headless' (sin ventana).
                Por defecto, True.
            browser_type (str, opcional): Tipo de navegador a utilizar
                (chromium, firefox o webkit). Por defecto, 'chromium'.

        Returns:
            playwright.sync_api.Page: Página lista para su uso.
        """
        if not cls._playwright:
            cls._playwright = sync_playwright().start()
        browser_launcher = getattr(cls._playwright, browser_type)
        cls._browser = browser_launcher.launch(
            headless=headless,
            args=["--start-maximized"],
        )
        cls._context = cls._browser.new_context()
        cls._page = cls._context.new_page()
        return cls._page

    @classmethod
    def get_page(cls):
        """Obtiene la página actual; si no existe, inicia un nuevo navegador.

        Returns:
            playwright.sync_api.Page: Página activa de Playwright.
        """
        if cls._page is None:
            cls.start_browser()
        return cls._page

    @classmethod
    def close_browser(cls):
        """Cierra el contexto, el navegador y detiene Playwright."""
        if cls._context:
            cls._context.close()
        if cls._browser:
            cls._browser.close()
        if cls._playwright:
            cls._playwright.stop()

    @classmethod
    def reset_context(cls):
        """Reinicia el contexto de navegación y crea una nueva página.

        Returns:
            playwright.sync_api.Page: Nueva página dentro del contexto reiniciado.
        """
        if cls._context:
            cls._context.close()
        cls._context = cls._browser.new_context()
        cls._page = cls._context.new_page()
        return cls._page
