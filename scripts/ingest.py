import os
import PyPDF2
from app.services.vector_service import VectorService
from app.core.logger import AppLogger

log = AppLogger("INGEST")


class TextExtractor:
    """Сервис для извлечения текста (Single Responsibility)"""

    @staticmethod
    def extract(file_path):
        ext = os.path.splitext(file_path)[1].lower()
        text = ""
        try:
            if ext == '.txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
            elif ext == '.pdf':
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        extracted = page.extract_text()
                        if extracted:
                            text += extracted + "\n"
            return text
        except Exception as e:
            log.error(f"Ошибка чтения {file_path}: {e}")
            return ""


def run_ingest():
    # Пути через абсолют, чтобы не зависеть от места запуска
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    folder_path = os.path.join(project_root, "data", "source")

    # Инициализируем базу (путь подхватится из дефолта VectorService или передай явно)
    db = VectorService(db_path=os.path.join(project_root, "data", "vector_db"))

    if not os.path.exists(folder_path):
        log.error(f"Папка не найдена: {folder_path}")
        return

    files = [f for f in os.listdir(folder_path) if not f.startswith('.')]
    if not files:
        log.warning("В папке source нет файлов!")
        return

    extractor = TextExtractor()

    for filename in files:
        file_path = os.path.join(folder_path, filename)
        log.info(f"--- Обработка файла: {filename} ---")

        content = extractor.extract(file_path)
        if not content:
            continue

        # Параметры нарезки
        chunk_size = 1200
        overlap = 150
        chunks = [content[i:i + chunk_size] for i in range(0, len(content), chunk_size - overlap)]

        log.info(f"Найдено {len(chunks)} частей. Начинаю загрузку...")

        success_count = 0
        for idx, chunk in enumerate(chunks):
            doc_id = f"{filename}_{idx}"
            try:
                # В VectorService уже есть свой try/except и логгер
                db.add_document(text=chunk, doc_id=doc_id)
                success_count += 1
            except Exception as e:
                log.error(f"Критический сбой на чанке {doc_id}: {e}")

        log.info(f"Результат {filename}: успешно {success_count} из {len(chunks)}")


if __name__ == "__main__":
    run_ingest()