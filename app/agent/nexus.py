from app.core.logger import AppLogger
from app.services.utils import clean_text
from app.ai.factory import ProviderFactory
from app.agent.prompter import AiPrompter
from app.services.intent_service import Intent

log = AppLogger("NEXUS_CORE")


class NexusAgent:
    def __init__(self, vector_db, intent_classifier):
        """Инъекция зависимостей: всё необходимое передается при создании"""
        self.vector_db = vector_db
        self.intent_service = intent_classifier
        self.prompter = AiPrompter()
        self.log = log

    async def chat(self, user_input: str, context_manager, stream_callback=None):
        try:
            query = clean_text(user_input)

            # 1. ОПРЕДЕЛЯЕМ НАМЕРЕНИЕ (Сначала это!)
            intent = await self.intent_service.classify(query)
            self.log.info(f"Detected intent: {intent.value}")

            # 2. СБОР КОНТЕКСТА (Только если нужно)
            docs = ""
            if intent in [Intent.TECH_TASK, Intent.KNOWLEDGE_QUERY]:
                docs = self.vector_db.query(query, n_results=5)
                self.log.info("RAG: Контекст извлечен из базы")
            else:
                self.log.info("RAG: Пропуск базы (SmallTalk/Junk)")

            # 3. ФОРМИРОВАНИЕ ПРОМПТА
            history = context_manager.get_context_string()
            provider = ProviderFactory.get_provider()

            messages = self.prompter.wrap_complex_query(
                query=query,
                context=docs,
                history=history
            )

            # 4. ЗАПРОС К ИИ
            response, _ = await provider.ask(messages, stream_callback=stream_callback)
            return response

        except Exception as e:
            self.log.error(f"Ошибка ядра Nexus: {e}")
            raise