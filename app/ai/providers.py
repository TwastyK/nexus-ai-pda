# app/ai/providers.py
import os
import asyncio
import json
from abc import ABC, abstractmethod
from google import genai
from app.core.logger import AppLogger

log = AppLogger("AI_PROVIDERS")


class BaseAI(ABC):
    @abstractmethod
    async def ask(self, messages: list, stream_callback=None):
        pass

    @abstractmethod
    async def generate_simple(self, prompt: str) -> str:
        pass


class GeminiProvider(BaseAI):
    def __init__(self, model="models/gemini-flash-latest"):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = model
        self.client = genai.Client(api_key=self.api_key)

    async def ask(self, messages: list, stream_callback=None):
        """Полноценный диалог с поддержкой Fallback на Ollama"""
        try:
            log.info(f"Gemini: запрос к {self.model_name} (streaming)...")
            system_instruction = next((m['content'] for m in messages if m['role'] == 'system'), "")

            formatted_contents = []
            for m in messages:
                if m['role'] == 'system': continue
                role = "user" if m['role'] == "user" else "model"
                formatted_contents.append({"role": role, "parts": [{"text": m['content']}]})

            def get_stream():
                return self.client.models.generate_content_stream(
                    model=self.model_name,
                    contents=formatted_contents,
                    config={'system_instruction': system_instruction, 'temperature': 0.2}
                )

            loop = asyncio.get_event_loop()
            response_stream = await loop.run_in_executor(None, get_stream)

            full_text = ""
            for chunk in response_stream:
                chunk_text = chunk.text or ""
                if chunk_text:
                    full_text += chunk_text
                    if stream_callback:
                        stream_callback(chunk_text)

            return full_text

        except Exception as e:
            if "429" in str(e) or "500" in str(e):
                log.warning(f" Gemini Node Failure: {e}. Switching to OLLAMA BACKUP...")
                # Автоматический переброс на локальную модель
                fallback = OllamaProvider()
                return await fallback.ask(messages, stream_callback)

            log.error(f"Критическая ошибка Gemini: {e}")
            raise

    async def generate_simple(self, prompt: str) -> str:
        """Метод для быстрых задач (интенты/JSON)"""
        try:
            log.info(f"Gemini: простой запрос к {self.model_name}...")
            res = self.client.models.generate_content(model=self.model_name, contents=prompt)
            return res.text or ""
        except Exception as e:
            if "429" in str(e):
                log.warning("Gemini Quota Full (Simple). Using Ollama...")
                fallback = OllamaProvider()
                return await fallback.generate_simple(prompt)
            return ""


class OllamaProvider(BaseAI):
    def __init__(self, model="qwen2.5-coder:3b"):
        self.model = model
        self.url = "http://127.0.0.1:11434/api/chat"

    async def ask(self, messages: list, stream_callback=None):
        import requests
        # Форматируем историю для Ollama (она понимает роль 'assistant')
        payload = {"model": self.model, "messages": messages, "stream": False}
        loop = asyncio.get_event_loop()

        def sync_req():
            try:
                response = requests.post(self.url, json=payload, timeout=10)
                return response.json()
            except Exception as e:
                return {"error": str(e)}

        res = await loop.run_in_executor(None, sync_req)

        if "error" in res:
            log.error(f"Ollama Critical Error: {res['error']}")
            return " [OFFLINE] Резервный узел Ollama недоступен.", None

        content = res['message']['content']
        if stream_callback:
            stream_callback(content)
        return content

    async def generate_simple(self, prompt: str) -> str:
        # Для простых задач используем тот же метод, но без стрима
        res = await self.ask([{"role": "user", "content": prompt}])
        return res