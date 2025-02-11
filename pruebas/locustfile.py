# locust -f locustfile.py
from locust import HttpUser, TaskSet, task, between
import random

# Datos de usuario para autenticación simulada
TEST_USERS = [
    {"username": "user1", "password": "pass123"},
    {"username": "user2", "password": "pass456"},
    {"username": "user3", "password": "pass789"}
]

class BrowseProducts(TaskSet):
    """Simula la navegación y búsqueda de productos"""
    
    @task(3)  # Más probabilidades de ejecutar esta tarea
    def view_product_list(self):
        """Ver la lista de productos"""
        self.client.get("/products")

    @task(2)
    def view_product_details(self):
        """Ver detalles de un producto aleatorio"""
        product_id = random.randint(1, 100)  # Simula 100 productos
        self.client.get(f"/products/{product_id}")

class UserBehavior(TaskSet):
    """Simula el comportamiento del usuario"""
    
    def on_start(self):
        """Se ejecuta al inicio de cada usuario para autenticarse"""
        self.user_data = random.choice(TEST_USERS)  # Seleccionar usuario aleatorio
        response = self.client.post("/login", json=self.user_data)
        
        if response.status_code == 200:
            self.token = response.json().get("token")
        else:
            self.token = None

    @task(5)
    def browse_products(self):
        """Simular navegación de productos"""
        self.client.get("/products")

    @task(3)
    def add_to_cart(self):
        """Añadir producto aleatorio al carrito"""
        product_id = random.randint(1, 100)
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        self.client.post(f"/cart/add", json={"product_id": product_id, "quantity": 1}, headers=headers)

    @task(2)
    def checkout(self):
        """Realizar compra si hay productos en el carrito"""
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        self.client.post("/checkout", headers=headers)

    @task(1)
    def logout(self):
        """Cerrar sesión"""
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        self.client.post("/logout", headers=headers)

class ECommerceUser(HttpUser):
    """Define el usuario de prueba"""
    
    host = "http://localhost:5000"  # Cambia esto por la URL de tu API
    wait_time = between(1, 3)  # Simula espera entre peticiones
    tasks = [UserBehavior, BrowseProducts]  # Asigna los conjuntos de tareas
