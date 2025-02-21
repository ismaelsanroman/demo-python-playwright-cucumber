# features/environment.py
"""Módulo de configuración de entorno para pruebas con Playwright."""

import asyncio
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from playwright.async_api import async_playwright

from utils.error_dictionary import ErrorDictionary


async def start_tracing(context):
    """Inicia el tracing en el contexto de Playwright."""
    await context.tracing.start(screenshots=True, snapshots=True, sources=True)


async def stop_tracing(context):
    """Detiene el tracing y guarda un archivo .zip en 'reports/traces/'.

    El nombre del archivo incluye fecha/hora para evitar sobreescrituras.
    """
    trace_dir = Path("reports/traces")
    trace_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    trace_path = trace_dir / f"trace_{timestamp}.zip"
    await context.tracing.stop(path=str(trace_path))


async def take_screenshot(page, scenario_name):
    """Toma una captura de pantalla y la guarda en 'reports/screenshots/'.

    El nombre del archivo incluye fecha/hora y el nombre del escenario.
    """
    screenshot_dir = Path("reports/screenshots")
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    scenario_safe_name = scenario_name.replace(" ", "_")
    screenshot_path = screenshot_dir / f"{scenario_safe_name}_{timestamp}.png"
    await page.screenshot(path=str(screenshot_path))
    print(f"🖼  Captura de pantalla guardada: {screenshot_path}")


def before_all(context):
    """Se ejecuta antes de cualquier test (feature).

    - Inicializa el loop de asyncio.
    - Inicia Playwright y el navegador.
    - Crea el browser_context y la page que usarán los escenarios.
    """
    load_dotenv()
    context.config.userdata = {
        "base_url": os.getenv("BASE_URL"),
        "api_url": os.getenv("API_URL"),
        "headless": os.getenv("HEADLESS"),
        "browser_type": os.getenv("BROWSER_TYPE"),
    }
    context.errors = ErrorDictionary()
    context.config.setup_logging()
    context.loop = asyncio.new_event_loop()
    asyncio.set_event_loop(context.loop)
    context.playwright = context.loop.run_until_complete(async_playwright().start())
    context.browser = context.loop.run_until_complete(
        context.playwright.chromium.launch(
            headless=False,
            args=["--start-maximized"],
            slow_mo=500,
        )
    )
    context.browser_context = context.loop.run_until_complete(
        context.browser.new_context()
    )
    context.page = context.loop.run_until_complete(context.browser_context.new_page())


def before_scenario(context, scenario):
    """Se ejecuta antes de cada escenario.

    - Inicia el tracing asíncrono en el contexto de Playwright.
    """
    if context.errors.has_errors():
        context.errors.clear_errors()
    context.loop.run_until_complete(start_tracing(context.browser_context))
    print(f"\n\n🚀 Iniciando escenario: '{scenario.name}'")


def after_scenario(context, scenario):
    """Se ejecuta después de cada escenario.

    - Si hay errores o el escenario falla, tomar screenshot.
    - Detener tracing y guardar el archivo .zip.
    - Imprimir y limpiar errores acumulados.
    """
    if scenario.status == "failed" or context.errors.has_errors():
        print(f"⚠️ El escenario '{scenario.name}' falló o acumuló errores.")
        context.loop.run_until_complete(take_screenshot(context.page, scenario.name))
    context.loop.run_until_complete(stop_tracing(context.browser_context))
    if context.errors.has_errors():
        for error in context.errors.get_all_errors():
            print(error)
        context.errors.clear_errors()


def after_all(context):
    """Se ejecuta una vez cuando se han corrido todas las features.

    - Cierra el contexto de navegador, el navegador y Playwright de forma asíncrona.
    - Cierra el event loop.
    """
    context.loop.run_until_complete(context.browser_context.close())
    context.loop.run_until_complete(context.browser.close())
    context.loop.run_until_complete(context.playwright.stop())
    context.loop.close()
    print("✅ Finalizada la ejecución de todas las pruebas.")
