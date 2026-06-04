from django.db import models
from django.utils import timezone
from django.urls import reverse


class HistoricalBuilding(models.Model):
    """Модель исторического здания"""
    
    STATUS_CHOICES = [
        ('draft', 'На модерации'),
        ('published', 'Опубликовано'),
        ('rejected', 'Отклонено'),
    ]
    
    CITY_CHOICES = [
        ('msk', 'Москва'),
        ('spb', 'Санкт-Петербург'),
        ('vlg', 'Волгоград'),
        ('other', 'Другой город'),
    ]
    
    # ========== ОСНОВНАЯ ИНФОРМАЦИЯ ==========
    name = models.CharField(max_length=200, verbose_name="Название здания")
    short_description = models.TextField(max_length=500, verbose_name="Краткое описание (для списка)")
    full_description = models.TextField(verbose_name="Полное описание для озвучки", blank=True)
    
    # ========== АРХИТЕКТУРНЫЕ ДЕТАЛИ ==========
    architect = models.CharField(max_length=200, blank=True, verbose_name="Архитектор")
    year_built = models.IntegerField(verbose_name="Год постройки")
    address = models.CharField(max_length=300, verbose_name="Адрес")
    architectural_style = models.CharField(max_length=100, blank=True, verbose_name="Архитектурный стиль")
    city = models.CharField(max_length=50, choices=CITY_CHOICES, default='other', verbose_name="Город")
    
    # ========== ДОСТУПНОСТЬ ДЛЯ НЕЗРЯЧИХ ==========
    tactile_features = models.TextField(blank=True, verbose_name="Тактильные особенности")
    sound_features = models.TextField(blank=True, verbose_name="Звуковое окружение")
    accessibility_notes = models.TextField(blank=True, verbose_name="Доступность для МГН")
    
    # ========== МЕДИАФАЙЛЫ ==========
    main_image = models.ImageField(upload_to='buildings/', blank=True, null=True, verbose_name="Главное изображение")
    audio_guide = models.FileField(upload_to='audio_guides/', blank=True, null=True, verbose_name="Аудиогид (MP3)")
    image_caption = models.TextField(blank=True, null=True, verbose_name="Описание изображения")
    
    # ========== КТО И КОГДА ДОБАВИЛ ==========
    suggested_by = models.CharField(max_length=200, verbose_name="Кто предложил добавить")
    suggested_email = models.EmailField(blank=True, verbose_name="Email для связи")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата добавления")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    # ========== МОДЕРАЦИЯ ==========
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Статус модерации")
    moderation_notes = models.TextField(blank=True, verbose_name="Примечания модератора")
    

class BuildingImage(models.Model):
    """Дополнительные изображения здания (галерея)"""
    building = models.ForeignKey(
        HistoricalBuilding, 
        on_delete=models.CASCADE, 
        related_name='images',
        verbose_name="Здание"
    )
    image = models.ImageField(upload_to='buildings/gallery/', verbose_name="Изображение")
    caption = models.CharField(max_length=200, blank=True, verbose_name="Подпись (озвучивается)")
    order = models.IntegerField(default=0, verbose_name="Порядок отображения")
    
    class Meta:
        ordering = ['order']
        verbose_name = "Изображение здания"
        verbose_name_plural = "Изображения зданий"
    
    def __str__(self):
        return f"Изображение для {self.building.name}"

class BuildingSuggestion(models.Model):
    """Модель для предложения НОВЫХ зданий от пользователей"""
    
    name = models.CharField(max_length=200, verbose_name="Название здания")
    city = models.CharField(
        max_length=50,
        choices=HistoricalBuilding.CITY_CHOICES,
        default='other',
        verbose_name="Город"
    )
    address = models.CharField(max_length=300, verbose_name="Адрес")
    description = models.TextField(verbose_name="Описание здания")
    
    suggested_by = models.CharField(max_length=200, verbose_name="Ваше имя")
    suggested_email = models.EmailField(verbose_name="Ваш Email")
    suggested_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата предложения"
    )
    
    is_processed = models.BooleanField(default=False, verbose_name="Обработано")
    processed_at = models.DateTimeField(blank=True, null=True, verbose_name="Дата обработки")
    notes = models.TextField(blank=True, verbose_name="Комментарий модератора")
    
    class Meta:
        ordering = ['-suggested_at']
        verbose_name = "Историческое здание"
        verbose_name_plural = "Исторические здания"
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('building_detail', args=[str(self.id)])