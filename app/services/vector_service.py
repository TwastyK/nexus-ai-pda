import os
import chromadb
from app.core.logger import AppLogger

log = AppLogger("VECTOR_SERVICE")

class VectorService:
    def __init__(self, db_path=None, threshold=1.5):
        self.threshold = threshold
        try:
            if db_path is None:
                project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                db_path = os.path.join(project_root, "data", "vector_db")

            os.makedirs(db_path, exist_ok=True)
            self.client = chromadb.PersistentClient(path=db_path)
            self.collection = self.client.get_or_create_collection(name="nexus_docs")
            log.info(f"База готова. Порог релевантности: {self.threshold}")
        except Exception as e:
            log.error(f"Сбой инициализации БД: {e}")
            raise

    def query(self, question: str, n_results=3):
        try:
            results = self.collection.query(query_texts=[question], n_results=n_results)
            if not results['documents'][0]: return ""

            dist = results['distances'][0][0]
            if dist > self.threshold:
                log.info(f"Контекст отклонен (dist: {dist:.2f} > {self.threshold})")
                return ""

            log.info(f"Найден релевантный контекст (dist: {dist:.2f})")
            return " ".join(results['documents'][0])
        except Exception as e:
            log.error(f"Ошибка поиска: {e}")
            return ""

    def add_document(self, text: str, doc_id: str):
        """Новый метод: Добавление текста в базу"""
        try:
            self.collection.add(
                documents=[text],
                ids=[doc_id]
            )
            log.info(f"Документ {doc_id} успешно записан в векторную базу")
            return True
        except Exception as e:
            log.error(f"Ошибка записи в БД: {e}")
            return False

    def get_stats(self):
        """Возвращает список имен всех загруженных документов"""
        try:
            # Получаем все метаданные из коллекции
            data = self.collection.get()
            ids = data.get('ids', [])
            return list(set([id.split('_')[0] for id in ids]))  # Чистим ID до имен файлов
        except Exception as e:
            log.error(f"Ошибка получения статистики БД: {e}")
            return []