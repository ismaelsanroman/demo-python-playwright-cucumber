Proyecto de Automatización con Python, Playwright y Behave

Este repositorio contiene un proyecto de automatización de pruebas (front y back) usando Python, Playwright y Behave (Cucumber en Python). También incluye prácticas de mocking de API, reportes con Allure, configuración en archivos YAML, uso de variables de entorno con .env y revisión de estilo con Flake8.

Estructura General del Proyecto

CURSO PYTHON-PLAYWRIGHT/
├── configs/
│   └── config.yaml
├── driver/
│   └── playwright_base.py
├── features/
│   ├── pages/
│   │   ├── base_page.py
│   │   ├── elements_page.py
│   │   ├── textbox_page.py
│   ├── steps/
│   │   ├── elements_steps.py
│   │   ├── environment.py
│   ├── textbox.feature
├── mocks/
├── reports/
│   ├── junit-results/
│   ├── screenshots/
│   ├── traces/
├── resources/
│   ├── testdata.yaml
│   ├── users.yaml
├── scripts/
│   └── run_tests.sh
├── utils/
│   ├── error_dictionary.py
│   ├── logger.py
├── venv/
├── .env
├── behave.ini
├── README.md
└── requirements.txt

1. Requisitos
Python 3.8+
pip
(Opcional) Java o Docker para ver reportes de Allure.
(Opcional) Flake8 para análisis de código.

2. Instalación
Clona el repositorio:
git clone <URL_DEL_REPOSITORIO>
cd CURSO PYTHON-PLAYWRIGHT

Crea y activa un entorno virtual:
python -m venv venv
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\activate  # Windows
Instala dependencias:
pip install -r requirements.txt
Instala los navegadores de Playwright:
playwright install

3. Variables de Entorno y Configuración
Ejemplo de .env:
BASE_URL=https://demoqa.com
HEADLESS=True
BROWSER_TYPE=chromium

Ajusta config.yaml según el entorno que uses.

4. Cómo Ejecutar las Pruebas
4.1 Pruebas con Behave
Para ejecutar todas las pruebas BDD:
behave
O bien, puedes usar tags para separar escenarios:
behave --tags=@front
behave --tags=@back

4.2 Generar Reporte Allure
behave \
  --format allure_behave.formatter:AllureFormatter \
  --alluredir=reports/allure-results

Luego generas y abres el reporte:
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report

4.3 Ejecución con Script
chmod +x scripts/run_tests.sh
./scripts/run_tests.sh

5. Mock Server (Pruebas de API)
Inicia el mock server:
python mocks/mock_server.py
Ejecuta pruebas relacionadas:
behave --tags=@back

6. Revisión de Estilo
Ejecuta Flake8 para comprobar la calidad del código:
flake8 .

7. Diseño y Principios
Page Object Model (POM) para modularización.
BDD con Cucumber para escenarios de prueba.
Logs detallados en cada interacción.
Diccionario de errores en utils/error_dictionary.py.

8. Futuras Mejoras
Ejecución paralela con behave-parallel o pytest-xdist.
CI/CD con GitHub Actions o Jenkins.
Pruebas de rendimiento con Locust o JMeter.

9. Contribuciones
Pull Requests bienvenidos.
Issues para reportar errores o solicitar mejoras.

10. Licencia
Especifica la licencia si aplica (ej. MIT License).