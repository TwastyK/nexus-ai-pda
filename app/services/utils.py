import re

def clean_text(text: str) -> str:
    """Очистка ввода от лишнего мусора, почты и карт (бывший Sanitizer)"""
    if not text: return ""
    # Оставляем только важную логику очистки
    text = re.sub(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', '[EMAIL]', text)
    text = re.sub(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b', '[CARD]', text)
    return text.strip()

def format_prompt(template: str, **kwargs) -> str:
    """Утилита для безопасной подстановки переменных в промпт"""
    return template.format(**kwargs)