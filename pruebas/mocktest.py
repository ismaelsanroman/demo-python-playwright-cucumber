from flask import Flask, jsonify
import threading
import requests
import time

# 1. Crear la API con Flask
app = Flask(__name__)

@app.route('/api/vegetales', methods=['GET'])
def get_vegetales():
    vegetales = [
        {"Name": "Fresa", "Type": "Fruta"},
        {"Name": "Manzana", "Type": "Fruta"},
        {"Name": "Zanahoria", "Type": "Verdura"},
        {"Name": "Platano", "Type": "Fruta"},
        {"Name": "Calabacín", "Type": "Verdura"},
        {"Name": "Pera", "Type": "Fruta"}
    ]
    return jsonify(vegetales)

# 2. Ejecutar Flask en un hilo para no bloquear el script
def run_api():
    app.run(port=5000)

api_thread = threading.Thread(target=run_api)
api_thread.daemon = True
api_thread.start()

# Esperamos un poco para que el servidor arranque
time.sleep(1)

# 3. Hacer la petición GET y procesar los datos
response = requests.get("http://127.0.0.1:5000/api/vegetales")

if response.status_code == 200:
    vegetales = response.json()
    errores = []
    
    for v in vegetales:
        if v["Type"] != "Fruta":
            errores.append(f"El elemento {v['Name']} no es una fruta")
    
    if errores:
        for error in errores:
            print(error)
    else:
        print("Todos los vegetales son frutas")
else:
    print(f"Error al obtener los datos de la API: {response.status_code}")
