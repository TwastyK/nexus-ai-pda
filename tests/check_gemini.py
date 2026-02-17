import os
from google import genai

# Прямо сюда вставь ключ для теста
client = genai.Client(api_key="AIzaSyB0OuWx6H0YPH0rLZeIl-wfCHSkKs7a73c")

try:
    print("Список доступных тебе моделей:")
    for model in client.models.list():
        # В новом SDK поле называется supported_generation_methods
        print(f"-> {model.name}")
except Exception as e:
    print(f"Ошибка: {e}")