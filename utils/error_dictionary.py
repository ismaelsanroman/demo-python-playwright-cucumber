# utils/error_dictionary.py
"""Módulo que define la clase `ErrorDictionary` para gestionar errores acumulados."""


class ErrorDictionary:
    """Clase para almacenar y gestionar una lista de errores."""

    def __init__(self):
        """Inicializa la lista de errores."""
        self.errors = []

    def add_error(self, error):
        """Agrega un error a la lista y lo imprime en consola.

        Args:
            error (str): Mensaje de error a almacenar.
        """
        print(f"🛑 {error}")
        self.errors.append(error)

    def has_errors(self):
        """Verifica si hay errores almacenados.

        Returns:
            bool: `True` si hay errores, `False` en caso contrario.
        """
        return len(self.errors) > 0

    def get_all_errors(self):
        """Devuelve la lista de errores almacenados.

        Returns:
            list: Lista de errores registrados.
        """
        return self.errors

    def clear_errors(self):
        """Limpia la lista de errores almacenados."""
        self.errors.clear()
