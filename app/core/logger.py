import logging


class AppLogger:
    def __init__(self, name: str):
        # Настраиваем стандартный логгер Python внутри нашего класса
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # Если у логгера еще нет обработчиков (чтобы не дублировать логи)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def info(self, message: str):
        self.logger.info(message)

    def error(self, message: str):
        self.logger.error(message)

    def warning(self, message: str):
        self.logger.warning(message)