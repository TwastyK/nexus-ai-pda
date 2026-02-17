import yaml
import os
from app.core.logger import AppLogger

log = AppLogger("PROMPTER")

class AiPrompter:
    def __init__(self, config_name="config.yaml"):
        # Прямой путь к твоей папке
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.config_path = os.path.join(base_path, "app", "promts", config_name)
        self.config = self._load_config()

    def _load_config(self):
        try:
            if os.path.exists(self.config_path):
                # utf-8-sig — это лекарство от UnicodeDecodeError: 0xff
                with open(self.config_path, 'r', encoding='utf-8-sig') as f:
                    data = yaml.safe_load(f)
                    log.info(f"SUCCESS: Конфиг подгружен: {self.config_path}")
                    return data if data else {}
            log.warning(f"CRITICAL: Конфиг не найден: {self.config_path}")
            return {}
        except Exception as e:
            log.error(f"Ошибка чтения конфига: {e}")
            return {}

    def wrap_complex_query(self, query: str, context: str, history: str) -> list:
        # Тянем данные из tech_expert (как в твоем файле)
        cfg = self.config.get('tech_expert', {})
        system_text = cfg.get('system', "Ты — Nexus, инженер.")
        user_template = cfg.get('user_template', "{context}\n\n{query}")

        user_text = user_template.format(history=history, context=context, query=query)
        return [
            {"role": "system", "content": system_text},
            {"role": "user", "content": user_text}
        ]