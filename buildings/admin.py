from django.contrib import admin
from django.utils.html import format_html
from .models import HistoricalBuilding, BuildingImage, BuildingSuggestion

class BuildingImageInline(admin.TabularInline):
    model = BuildingImage
    extra = 1
    fields = ['image', 'caption', 'order']

@admin.register(HistoricalBuilding)
class HistoricalBuildingAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'year_built', 'architect', 'suggested_by', 'created_at', 'status']
    list_filter = ['status', 'city', 'architectural_style', 'created_at']  # Добавили city в фильтры
    search_fields = ['name', 'address', 'architect', 'city']
    readonly_fields = ['created_at', 'updated_at', 'image_preview']
    inlines = [BuildingImageInline]
    
    fieldsets = (
        (' Основная информация', {
            'fields': ('name', 'city', 'short_description', 'full_description', 'status')
        }),
        (' Архитектурные данные', {
            'fields': ('architect', 'year_built', 'address', 'architectural_style')
        }),
        (' Доступность для незрячих', {
            'fields': ('tactile_features', 'sound_features', 'accessibility_notes')
        }),
        (' Медиа', {
            'fields': ('main_image', 'image_preview', 'audio_guide')
        }),
        (' Информация о добавлении', {
            'fields': ('suggested_by', 'suggested_email', 'created_at', 'updated_at')
        }),
        (' Модерация', {
            'fields': ('moderation_notes',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" width="100" height="100" style="border-radius: 8px;" />', obj.main_image.url)
        return "Нет изображения"
    image_preview.short_description = "Превью"

@admin.register(BuildingSuggestion)
class BuildingSuggestionAdmin(admin.ModelAdmin):
    list_display = ['name', 'suggested_by', 'suggested_at', 'is_processed']
    list_filter = ['is_processed', 'suggested_at']
    search_fields = ['name', 'address', 'suggested_by', 'suggested_email']
    readonly_fields = ['suggested_at']
    
    actions = ['mark_as_processed']
    
    def mark_as_processed(self, request, queryset):
        from django.utils import timezone
        queryset.update(is_processed=True, processed_at=timezone.now())
    mark_as_processed.short_description = "Отметить как обработанные"