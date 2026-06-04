# test_signal.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'historical_buildings_site.settings')
django.setup()

from buildings.models import HistoricalBuilding

building = HistoricalBuilding.objects.create(
    name="Тестовое здание",
    short_description="Краткое описание",
    full_description="",
    year_built=2024,
    address="Тестовый адрес",
    suggested_by="Тестер",
    status="published"
)

print(f"Создано здание: {building.name}")
print(f"full_description после сохранения: {building.full_description}")