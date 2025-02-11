import asyncio
import re
from logging import handlers
from playwright.async_api import async_playwright, expect, Page

# async def main():
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=False)
#         page = await browser.new_page()
#         await page.goto("https://www.google.es/")
#         print("*Título: ", await page.title())
#         await browser.close()

# asyncio.run(main())

    # await page.pause()
    # await asyncio.sleep(10)
    # input("🔴 Test pausado. Presiona Enter para continuar...")

async def launch_driver(p):
    """Inicializa Playwright y devuelve el navegador y la página."""
    print("\n🚀 Iniciando pruebas")
    browser = await p.chromium.launch(headless=False, slow_mo=500)

    context = await browser.new_context()
    await context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page = await context.new_page()
    
    await goto_page(page, "https://www.google.es/")
    await obtain_title(page, "Google")
    await cookie_accept(page)
    await search_item(page)
    await close_driver(browser, context)

async def goto_page(page, web):
    print(f"🌍 Navegando a {web}...")
    await page.goto(web)
    await expect(page).to_have_url(re.compile(web))

async def obtain_title(page, name):
    """Obtiene e imprime el título de la página y lo valida."""
    print("🔍 Obteniendo título de la página...")
    await page.title()
    await expect(page).to_have_title(re.compile(name))

async def cookie_accept(page):
    """Hace clic en el botón de aceptar cookies."""
    try:
        await page.locator("//div[text()='Aceptar todo']").click()
        print("🍪 Cookies aceptadas...")
    except:
        print("⚠️ No se encontró el botón de cookies.")
        
async def search_item(page):
    """Escribe un término en la barra de búsqueda y muestra los resultados."""
    print("📝 Realizando búsqueda en Google...")
    buscador = page.locator("//textarea[@title='Buscar']")
    await buscador.fill("Playwright en Python")
    await buscador.press("Enter")
    print("⌛ Esperando a que aparezcan los resultados...")
    await page.locator("#search").wait_for()

    titulos = await page.locator("h3").evaluate_all("els => els.map(el => el.textContent.trim())")
    print("\n🔍 **Resultados de la búsqueda:**")
    for i, titulo in enumerate(titulos, 1):
        print(f"  🔹 Resultado {i}: {titulo}")
    await page.screenshot(path="../reports/screenshots/testAsync.png")

async def close_driver(browser, context):
    """Cierra el navegador."""
    await context.tracing.stop(path="../reports/traces/trace.zip")
    await browser.close()
    print("❌ Cerrando el navegador...")

async def main():
    print("🎭 Iniciando Playwright...")
    p = await async_playwright().start()
    await launch_driver(p)
    await p.stop()

asyncio.run(main())
