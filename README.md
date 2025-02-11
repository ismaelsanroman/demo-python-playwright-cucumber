# 🧪 Demo Automation Testing con Python, Playwright y Cucumber

## 📌 Descripción
Este proyecto automatiza pruebas de interfaz de usuario (UI) utilizando **Python**, **Playwright** y **Behave** (BDD con Cucumber/Gherkin).  
Se enfoca en la interacción con la página [DemoQA](https://demoqa.com/) y permite realizar pruebas E2E con trazas, capturas de pantalla y mocks de API.

---

## 🚀 Tecnologías utilizadas

🔹 **Python** (Lenguaje principal)  
🔹 **Playwright** (Automatización del navegador)  
🔹 **Behave** (Framework BDD estilo Cucumber)  
🔹 **Flask** (Mock server para pruebas API)  
🔹 **Allure** (Opcional para generación de reportes)  
🔹 **Pre-commit** (Estilo de código: Black, isort, flake8)  

---

## 📂 Estructura del proyecto

📦 demo-python-playwright-cucumber ├── 📂 configs # Archivos de configuración │ └── config.yaml # Configuración personalizada ├── 📂 driver # Clases base para gestionar Playwright │ └── playwright_base.py ├── 📂 features # Pruebas BDD en Gherkin │ ├── 📂 pages # Page Object Model (POM) │ │ ├── base_page.py │ │ ├── elements_page.py │ │ └── textbox_page.py │ ├── 📂 steps # Implementación de los steps en Python │ │ ├── environment.py # Configuración global de Behave │ │ ├── textbox_steps.py │ ├── textbox.feature # Escenarios de prueba en Gherkin ├── 📂 mocks # Servidor Flask para pruebas API │ └── mock_server.py ├── 📂 reports # Reportes de ejecución y capturas │ ├── junit-results/ │ ├── screenshots/ │ ├── traces/ ├── 📂 resources # Datos de prueba en YAML │ ├── testdata.yaml │ ├── users.yaml ├── 📂 scripts # Scripts auxiliares │ └── run_tests.sh # Script para ejecutar pruebas ├── 📂 utils # Utilidades (logs, manejo de errores) │ ├── error_dictionary.py │ ├── logger.py ├── .env # Variables de entorno ├── .flake8 # Configuración de Flake8 ├── .gitignore # Archivos ignorados en Git ├── .pre-commit-config.yaml # Configuración de pre-commit ├── behave.ini # Configuración de Behave ├── LICENSE # Licencia del proyecto ├── pyproject.toml # Configuración de formateo de código ├── README.md # 📖 Documentación del proyecto └── requirements.txt # 📦 Dependencias del proyecto

yaml
Copiar
Editar

---

## ⚙️ Instalación

### 🔹 1. Clonar el repositorio
```sh
git clone https://github.com/tu-usuario/demo-python-playwright-cucumber.git
cd demo-python-playwright-cucumber
🔹 2. Crear un entorno virtual
sh
Copiar
Editar
python -m venv venv
Activar el entorno:

Windows:
sh
Copiar
Editar
venv\Scripts\activate
Mac/Linux:
sh
Copiar
Editar
source venv/bin/activate
🔹 3. Instalar dependencias
sh
Copiar
Editar
pip install -r requirements.txt
🔹 4. Instalar los hooks de pre-commit (opcional pero recomendado)
sh
Copiar
Editar
pre-commit install
Esto asegurará que Black, isort y flake8 se ejecuten antes de cada commit.

🏃‍♂️ Ejecución de las pruebas
🔹 1. Ejecutar los tests con Behave
sh
Copiar
Editar
behave
Si deseas generar reportes JUnit o Allure, ajusta los formatos y rutas de salida, por ejemplo:

sh
Copiar
Editar
behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results
🔹 2. (Opcional) Generar reporte de Allure
sh
Copiar
Editar
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
Asegúrate de instalar Allure CLI si no lo tienes.

🔹 3. (Opcional) Ejecutar el mock server
Si necesitas probar el consumo de un endpoint simulado:

sh
Copiar
Editar
python mocks/mock_server.py
El servidor se iniciará en http://localhost:5000/mock-endpoint.

📝 Ejemplo de Escenario BDD
Archivo: features/textbox.feature

gherkin
Copiar
Editar
Feature: Formulario de TextBox en DemoQA

  Scenario: Rellenar y verificar formulario
    Given I navigate to DemoQA and "Elements" Page
    When I open the "Text Box" section
    Then I fill in the form with the following data
      | name  | email               | current_address   | permanent_address   |
      | John  | john@example.com    | Main Street, 123  | Second Street, 456  |
    Then I verify the form with the following data
      | name  | email               | current_address   | permanent_address   |
      | John  | john@example.com    | Main Street, 123  | Second Street, 456  |
💡 Notas adicionales
Variables de entorno:

Puedes definir valores en el archivo .env (por ej. BASE_URL) y cargarlos desde los steps (environment.py).
Control de Errores:

El archivo utils/error_dictionary.py permite acumular errores sin detener la ejecución completa.
Revisiones de código (pre-commit):

Se configuran hooks que ejecutan Black, isort y flake8 para forzar un estilo uniforme y detección temprana de errores.
Requerimientos adicionales:

Asegúrate de tener Node.js instalado si usas ciertas funciones avanzadas de Playwright (puede requerirlo para drivers).
📃 Licencia
Este proyecto se distribuye bajo la licencia MIT. Puedes usarlo y adaptarlo libremente.

📧 Contacto:
📧 Email
🤖 GitHub

