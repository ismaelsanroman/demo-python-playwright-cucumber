#!/bin/bash

# =============================================================================
# 🛠 RUN_TESTS.SH - SCRIPT DE EJECUCIÓN AUTOMATIZADA
# -----------------------------------------------------------------------------
#  - Activa el entorno virtual (o lo crea si no existe)
#  - Instala dependencias si es necesario
#  - Inicia el servidor mock en segundo plano
#  - Ejecuta las pruebas con Behave y genera los resultados para Allure
#  - Reintenta automáticamente los tests fallidos
#  - Genera el reporte Allure en HTML y lo abre en el navegador
#  - Detiene el servidor mock al finalizar
# =============================================================================

set -e  # Si un comando falla, el script termina

# 0) CONFIGURACIÓN OPCIONAL - Permite ejecutar pruebas con tags específicos
TAGS=$1  # Ejemplo: @smoke, @regression, @api
if [ -z "$TAGS" ]; then
  TAGS=""  # Si no se pasan tags, ejecuta todas las pruebas
fi

# -----------------------------------------------------------------------------#
# 1) ACTIVAR O CREAR ENTORNO VIRTUAL
# -----------------------------------------------------------------------------#
if [ ! -d "venv" ]; then
  echo "🛠  No se encontró el entorno virtual (venv). Creándolo..."
  python -m venv venv
fi

echo "✅ Activando el entorno virtual..."
# Compatibilidad con Windows y Linux/macOS
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate  # Windows
else
    source venv/bin/activate  # Linux/macOS
fi

# -----------------------------------------------------------------------------#
# 2) INSTALAR DEPENDENCIAS
# -----------------------------------------------------------------------------#
echo "🔍 Instalando dependencias (si hay cambios en requirements.txt)..."
pip install --upgrade pip
pip install -r requirements.txt

# Asegura que Playwright tenga los navegadores instalados
playwright install --with-deps

# -----------------------------------------------------------------------------#
# 3) INICIAR SERVIDOR MOCK EN BACKGROUND
# -----------------------------------------------------------------------------#
echo "🚀 Iniciando servidor mock en segundo plano..."
python mocks/mock_server.py &
MOCK_PID=$!

# Opcional: esperar unos segundos a que levante el servidor
sleep 3

# -----------------------------------------------------------------------------#
# 4) EJECUTAR PRUEBAS CON BEHAVE + GUARDAR FALLAS
# -----------------------------------------------------------------------------#
echo "⚙️  Ejecutando pruebas con Behave (tags: $TAGS)..."
behave -f allure_behave.formatter:AllureFormatter \
       -o reports/allure-results \
       --no-skipped \
       --junit \
       --outfile=rerun.failures.txt \
       --tags="$TAGS"

# -----------------------------------------------------------------------------#
# 5) REEJECUTAR TESTS FALLIDOS (SI EXISTEN)
# -----------------------------------------------------------------------------#
if [[ -s rerun.failures.txt ]]; then
    echo "🔄 Reintentando pruebas fallidas..."
    behave @rerun.failures.txt
fi

# -----------------------------------------------------------------------------#
# 6) GENERAR REPORTE ALLURE Y ABRIRLO
# -----------------------------------------------------------------------------#
if ! command -v allure &> /dev/null; then
    echo "❌ Allure no está instalado. Por favor, instálalo para ver los reportes."
    exit 1
fi

echo "📊 Generando reporte Allure..."
allure generate reports/allure-results -o reports/allure-report --clean

echo "🌐 Abriendo reporte Allure en el navegador..."
allure open reports/allure-report

# -----------------------------------------------------------------------------#
# 7) DETENER SERVIDOR MOCK
# -----------------------------------------------------------------------------#
echo "🛑 Deteniendo servidor mock (PID=$MOCK_PID)..."
kill $MOCK_PID 2>/dev/null || echo "⚠️ No se pudo detener el servidor mock."

echo "✅ Proceso de pruebas finalizado correctamente."
exit 0
