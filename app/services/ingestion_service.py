import os
import glob
from app.core.logger import AppLogger

log = AppLogger("INGESTION_SERVICE")


class IngestionService:
    def __init__(self, vector_db):
        self.db = vector_db
        self.allowed_formats = {'.txt', '.md', '.py', '.yaml'}

    async def process(self, source: str) -> bool:
        """
        Универсальный обработчик.
        Принимает путь к файлу, папке или URL.
        """
        try:
            if not source:
                return False

            # Если это ссылка
            if source.startswith(("http://", "https://")):
                return await self._process_url(source)

            # Если передан путь (файл или папка)
            target = os.path.abspath(source)
            if os.path.isfile(target):
                return await self._process_file(target)
            elif os.path.isdir(target):
                return await self._process_folder(target)

            log.error(f"Путь не найден: {source}")
            return False
        except Exception as e:
            log.error(f"Ошибка при обработке {source}: {e}")
            return False

    async def _process_file(self, path: str) -> bool:
        """Логика чтения одного файла"""
        try:
            ext = os.path.splitext(path)[1].lower()
            if ext not in self.allowed_formats:
                return False

            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            if content.strip():
                # ID = имя_файла + размер (простая проверка на уникальность)
                doc_id = f"{os.path.basename(path)}_{os.path.getsize(path)}"
                self.db.add_document(content, doc_id)
                log.info(f"Документ загружен: {os.path.basename(path)}")
                return True
            return False
        except Exception as e:
            log.error(f"Не удалось прочитать файл {path}: {e}")
            return False

    async def _process_folder(self, folder_path: str):
        """Массовая загрузка из папки"""
        log.info(f"Сканирование директории: {folder_path}")
        for root, _, files in os.walk(folder_path):
            for file in files:
                await self._process_file(os.path.join(root, file))
        return True