from app.ai.providers import GeminiProvider, OllamaProvider
from app.core.logger import AppLogger
import os

log = AppLogger("FACTORY")

class ProviderFactory:
    @staticmethod
    def get_provider(is_complex: bool = True):
        try:
            # Если есть ключ Gemini — это наш приоритет №1
            if os.getenv("GEMINI_API_KEY"):
                log.info("Выбран Gemini (Cloud)")
                return GeminiProvider()

            # Если ключа нет — катимся на локалку
            log.info("Выбрана Ollama (Local)")
            return OllamaProvider()
        except Exception as e:
            log.error(f"Ошибка фабрики: {e}")
            return OllamaProvider()