# test_yandex.py
import os
import django
import requests

# Настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'historical_buildings_site.settings')
django.setup()

from django.conf import settings

print(" Тестируем подключение к YandexGPT...")
print(f"Folder ID: {getattr(settings, 'YANDEX_FOLDER_ID', 'НЕ ЗАДАН')}")
print(f"API Key: {'ЗАДАН' if getattr(settings, 'YANDEX_API_KEY', None) else 'НЕ ЗАДАН'}")

if not hasattr(settings, 'YANDEX_FOLDER_ID') or not hasattr(settings, 'YANDEX_API_KEY'):
    print(" Ошибка: YANDEX_FOLDER_ID или YANDEX_API_KEY не заданы в settings.py")
    print("Добавьте их в конец файла historical_buildings_site/settings.py:")
    print("YANDEX_FOLDER_ID = 'ваш_folder_id'")
    print("YANDEX_API_KEY = 'ваш_api_ключ'")
    exit()

# Тестовый запрос к YandexGPT
url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Api-Key {settings.YANDEX_API_KEY}"
}

body = {
    "modelUri": f"gpt://{settings.YANDEX_FOLDER_ID}/yandexgpt-lite",
    "completionOptions": {
        "stream": False,
        "temperature": 0.6,
        "maxTokens": 200
    },
    "messages": [
        {"role": "system", "text": "Ты помощник. Отвечай кратко."},
        {"role": "user", "text": "Назови столицу России"}
    ]
}

print("Отправляем тестовый запрос...")

try:
    response = requests.post(url, headers=headers, json=body, timeout=30)
    print(f"Статус ответа: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        answer = result['result']['alternatives'][0]['message']['text']
        print(f" Ответ YandexGPT: {answer}")
    else:
        print(f" Ошибка API: {response.text}")
        
except Exception as e:
    print(f" Исключение: {e}")