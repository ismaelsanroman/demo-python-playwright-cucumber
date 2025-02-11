import re
from playwright.sync_api import sync_playwright, expect

def launch_driver(p):
    """Inicializa Playwright y ejecuta las pruebas en secuencia."""
    print("\n🚀 Iniciando pruebas")
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    goto_page(page, "https://www.google.es/")
    obtain_title(page, "Google")
    cookie_accept(page)
    search_item(page)
    close_driver(browser)

def goto_page(page, web):
    """Navega a la página deseada."""
    print(f"🌍 Navegando a {web}...")
    page.goto(web)

def obtain_title(page, name):
    """Obtiene e imprime el título de la página y lo valida."""
    print(f"🔍 Verificando título '{name}' de la página...")
    page.title()
    expect(page).to_have_title(re.compile(name))

def cookie_accept(page):
    """Hace clic en el botón de aceptar cookies."""
    page.locator("//div[text()='Aceptar todo']").click()
    print("🍪 Cookies aceptadas...")

def search_item(page):
    """Escribe un término en la barra de búsqueda y muestra los resultados."""
    print("📝 Realizando búsqueda en Google...")
    buscador = page.locator("//textarea[@title='Buscar']")
    buscador.fill("Playwright en Python")
    buscador.press("Enter")
    print("⌛ Esperando a que aparezcan los resultados...")
    page.locator("#search").wait_for()

    titulos = page.locator("h3").evaluate_all("els => els.map(el => el.textContent.trim())")
    print("\n🔍 **Resultados de la búsqueda:**")
    for i, titulo in enumerate(titulos, 1):
        print(f"  🔹 Resultado {i}: {titulo}")

    page.screenshot(path="../reports/screenshots/testSync.png")

def close_driver(browser):
    """Cierra el navegador."""
    browser.close()
    print("❌ Cerrando el navegador...")

def main():
    print("🎭 Iniciando Playwright...")
    with sync_playwright() as p:
        launch_driver(p)
    print("✅ Pruebas finalizadas.")

main()
