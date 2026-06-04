# test_signal.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'historical_buildings_site.settings')
django.setup()

from buildings.models import HistoricalBuilding
from buildings.yandex_gpt import get_generator

print("🔍 Проверка работы генератора...")

test_building = HistoricalBuilding(
    name="Собор Василия Блаженного",
    short_description="Знаменитый собор на Красной площади",
    full_description="",  # Пустое поле
    year_built=1561,
    address="Москва, Красная площадь",
    suggested_by="Тестер",
    status="published"
)

print(f"Тестовое здание: {test_building.name}")
print(f"full_description ДО генерации: '{test_building.full_description}'")
print("Запускаем генерацию...")

generator = get_generator()
description = generator.generate_description(
    building_name=test_building.name,
    year_built=test_building.year_built,
    city="Москва"
)

print(f"\nСгенерированное описание:")
print(description[:300] + "..." if len(description) > 300 else description)

test_building.full_description = description
print(f"\n✅ full_description ПОСЛЕ генерации: {len(description)} символов")