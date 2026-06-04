# buildings/yandex_gpt.py
import requests
from django.conf import settings

class YandexGPTGenerator:
    """
    Класс для генерации описаний зданий через YandexGPT
    """
    
    def __init__(self):
        self.folder_id = getattr(settings, 'YANDEX_FOLDER_ID', None)
        self.api_key = getattr(settings, 'YANDEX_API_KEY', None)
        self.url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    
    def generate_description(self, building_name, architect=None, year_built=None, city=None):
        """
        Генерирует историческое описание здания на русском языке
        """
        if not self.folder_id or not self.api_key:
            print("❌ Ошибка: YANDEX_FOLDER_ID или YANDEX_API_KEY не заданы в settings.py")
            return f"{building_name}. Описание временно недоступно. Пожалуйста, добавьте здание позже."
        
        context_parts = [f"Название: {building_name}"]
        if architect:
            context_parts.append(f"Архитектор: {architect}")
        if year_built:
            context_parts.append(f"Год постройки: {year_built}")
        if city:
            context_parts.append(f"Город: {city}")
        
        context = ", ".join(context_parts)
        
        system_prompt = (
            "Ты — опытный экскурсовод по историческим зданиям. Твоя задача — понятно и интересно "
            "описывать архитектуру для незрячих людей. Используй простой русский язык, "
            "избегай сложных терминов. Описание должно быть объёмом 150-250 слов."
        )
        
        user_prompt = (
            f"Напиши подробное описание для здания: {context}. "
            f"Включи: 1) историческую справку, 2) архитектурные особенности, "
            f"3) что можно почувствовать или услышать рядом с этим зданием."
        )
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {self.api_key}"
        }
        
        body = {
            "modelUri": f"gpt://{self.folder_id}/yandexgpt-lite",
            "completionOptions": {
                "stream": False,
                "temperature": 0.7,
                "maxTokens": 1000
            },
            "messages": [
                {"role": "system", "text": system_prompt},
                {"role": "user", "text": user_prompt}
            ]
        }
        
        try:
            response = requests.post(self.url, headers=headers, json=body, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                description = result['result']['alternatives'][0]['message']['text']
                print(f"✅ Описание для '{building_name}' успешно сгенерировано")
                return description
            else:
                print(f" Ошибка API: {response.status_code} - {response.text}")
                return f"{building_name}. Описание временно недоступно. Попробуйте позже."
                
        except requests.exceptions.Timeout:
            print(" Таймаут запроса к YandexGPT")
            return f"{building_name}. Сервер временно не отвечает. Попробуйте позже."
        except Exception as e:
            print(f" Ошибка: {e}")
            return f"{building_name}. Не удалось сгенерировать описание."

# Глобальный экземпляр
generator = None

def get_generator():
    global generator
    if generator is None:
        generator = YandexGPTGenerator()
    return generator