# utils/logger.py
"""Módulo define la clase `Logger` para configurar y obtener un logger compartido."""

import logging


class Logger:
    """Clase singleton para la configuración y uso de un logger en la aplicación."""

    _logger = None

    def __init__(self, name="test-logger"):
        """Inicializa el logger con un formato estándar y un manejador de consola.

        Args:
            name (str, opcional): Nombre del logger. Por defecto, 'test-logger'.
        """
        if not Logger._logger:
            Logger._logger = logging.getLogger(name)
            Logger._logger.setLevel(logging.DEBUG)
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            console_handler.setFormatter(formatter)
            Logger._logger.addHandler(console_handler)

    def get_logger(self):
        """Obtiene la instancia única del logger configurado.

        Returns:
            logging.Logger: Instancia del logger.
        """
        return Logger._logger
