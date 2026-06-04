# generate_audio_for_existing.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'historical_buildings_site.settings')
django.setup()

from buildings.models import HistoricalBuilding
from buildings.tts_generator import get_audio_generator

audio_gen = get_audio_generator()
buildings = HistoricalBuilding.objects.filter(full_description__isnull=False, audio_guide__isnull=True)

print(f"🔍 Найдено зданий без аудио: {buildings.count()}")

for building in buildings:
    print(f"Обработка: {building.name}")
    audio_path = audio_gen.text_to_audio(
        text=building.full_description,
        building_id=building.id,
        building_name=building.name
    )
    
    if audio_path:
        building.audio_guide = audio_path
        building.save()
        print(f"Готово: {building.name}")
    else:
        print(f"Ошибка: {building.name}")

print("🏁 Завершено!")