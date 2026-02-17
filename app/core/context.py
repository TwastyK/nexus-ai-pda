from app.core.logger import AppLogger

log = AppLogger("CONTEXT_MANAGER")


class ContextManager:
    def __init__(self, max_history: int = 5):
        # Храним историю в памяти (потом перенесем в БД)
        self.history = []
        self.max_history = max_history

    def add_message(self, role: str, content: str):
        """Добавляет сообщение в историю и обрезает ее, если она слишком длинная"""
        self.history.append({"role": role, "content": content})

        if len(self.history) > self.max_history * 2:  # *2 потому что пара юзер-бот
            self.history = self.history[-self.max_history * 2:]
            log.info("История сообщений была обрезана для экономии контекста")

    def get_context_string(self) -> str:
        """Превращает историю в одну строку для промпта"""
        context_str = ""
        for msg in self.history:
            prefix = "User" if msg["role"] == "user" else "Assistant"
            context_str += f"{prefix}: {msg['content']}\n"
        return context_str

    def clear(self):
        self.history = []
        log.info("Память контекста очищена")