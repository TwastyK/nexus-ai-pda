import requests

# ВСТАВЬ СЮДА СВОЙ КЛЮЧ ИЗ AI STUDIO (БЕЗ ПРОБЕЛОВ)
API_KEY = "YOUR GEMINI CODE"

# Ссылка версии v1 (самая стабильная)
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"
payload = {
    "contents": [{
        "parts": [{"text": "Write a short python code"}]
    }]
}
headers = {'Content-Type': 'application/json'}

try:
    print(f"--- ОТПРАВКА ЗАПРОСА (v1) ---")
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    print(f"Статус: {response.status_code}")
    if response.status_code == 200:
        print("ПОБЕДА! Gemini ответил.")
        print(response.json()['candidates'][0]['content']['parts'][0]['text'][:100] + "...")
    else:
        print(f"Ошибка: {response.text}")
except Exception as e:
    print(f"Ошибка в коде: {e}")