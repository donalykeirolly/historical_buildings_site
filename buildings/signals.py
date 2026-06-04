# buildings/signals.py
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import HistoricalBuilding
from .yandex_gpt import get_generator
from .tts_generator import get_audio_generator
import os

@receiver(pre_save, sender=HistoricalBuilding)
def generate_description_from_name(sender, instance, **kwargs):
    """
    Генерирует описание здания через YandexGPT на основе названия.
    """
    # Если описание уже есть и длинное — пропускаем
    if instance.full_description and len(instance.full_description) > 100:
        print(f"⏭ Описание для '{instance.name}' уже есть. Генерация пропущена.")
        return
    
    print(f" Генерирую описание для '{instance.name}'...")
    
    generator = get_generator()
    description = generator.generate_description(
        building_name=instance.name,
        architect=instance.architect if instance.architect else None,
        year_built=instance.year_built if instance.year_built else None,
        city=instance.get_city_display() if instance.city else None
    )
    
    instance.full_description = description
    print(f" Описание сохранено для '{instance.name}'")


@receiver(post_save, sender=HistoricalBuilding)
def generate_audio_for_building(sender, instance, created, **kwargs):
    """
    СОЗДАЁТ АУДИОГИД ПОСЛЕ СОХРАНЕНИЯ ОПИСАНИЯ
    Запускается после того, как описание уже сохранено в базу
    """
    if not instance.full_description:
        print(f"⚠️ Нет текста описания для '{instance.name}', аудио не создано")
        return
    
    if instance.audio_guide and os.path.exists(instance.audio_guide.path):
        print(f"Аудиогид для '{instance.name}' уже существует")
        return
    
    print(f"Создаю аудиогид для '{instance.name}'...")
    
    # Генерируем аудио из текста
    audio_gen = get_audio_generator()
    audio_path = audio_gen.text_to_audio(
        text=instance.full_description,
        building_id=instance.id,
        building_name=instance.name
    )
    
    if audio_path:
        # Сохраняем путь к аудиофайлу в модель
        instance.audio_guide = audio_path
        # Используем save() без сигналов, чтобы избежать рекурсии
        sender.objects.filter(pk=instance.pk).update(audio_guide=audio_path)
        print(f"Аудиогид для '{instance.name}' сохранён")
    else:
        print(f"Не удалось создать аудиогид для '{instance.name}'")