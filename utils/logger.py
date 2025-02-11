# utils/logger.py
import logging

class Logger:
    _logger = None

    def __init__(self, name='test-logger'):
        if not Logger._logger:
            Logger._logger = logging.getLogger(name)
            Logger._logger.setLevel(logging.DEBUG)
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            Logger._logger.addHandler(console_handler)

    def get_logger(self):
        return Logger._logger
