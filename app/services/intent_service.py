import logging
from enum import Enum

class Intent(Enum):
    SMALL_TALK = "small_talk"
    TECH_TASK = "tech_task"
    KNOWLEDGE_QUERY = "query"
    JUNK = "junk"

class IntentClassifier:
    def __init__(self, ai_provider):
        self.ai = ai_provider
        self.log = logging.getLogger("NEXUS_INTENT")

    async def classify(self, text: str) -> Intent:
        if len(text.split()) < 2: return Intent.SMALL_TALK # Слишком коротко
        try:
            # Даем ИИ жесткую команду на одно слово
            prompt = f"Identify category: 'small_talk', 'tech_task', 'junk'. Input: '{text}'. Result (1 word):"
            res = await self.ai.generate_simple(prompt)
            label = res.strip().lower()

            if "tech" in label: return Intent.TECH_TASK
            if "small" in label: return Intent.SMALL_TALK
            return Intent.JUNK
        except:
            return Intent.TECH_TASK # Безопасный режим