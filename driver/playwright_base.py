# driver/playwright_base.py
import asyncio

from playwright.sync_api import sync_playwright


class PlaywrightBase:
    _playwright = None
    _browser = None
    _context = None
    _page = None

    @classmethod
    def start_browser(cls, headless=True, browser_type="chromium"):
        if not cls._playwright:
            cls._playwright = sync_playwright().start()
        browser_launcher = getattr(cls._playwright, browser_type)
        cls._browser = browser_launcher.launch(
            headless=headless, args=["--start-maximized"]
        )
        cls._context = cls._browser.new_context()
        cls._page = cls._context.new_page()
        return cls._page

    @classmethod
    def get_page(cls):
        if cls._page is None:
            cls.start_browser()
        return cls._page

    @classmethod
    def close_browser(cls):
        if cls._context:
            cls._context.close()
        if cls._browser:
            cls._browser.close()
        if cls._playwright:
            cls._playwright.stop()

    @classmethod
    def reset_context(cls):
        # Útil si deseas re-inicializar
        if cls._context:
            cls._context.close()
        cls._context = cls._browser.new_context()
        cls._page = cls._context.new_page()
        return cls._page
