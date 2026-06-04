from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import HistoricalBuilding, BuildingSuggestion
from .forms import BuildingSuggestionForm

def index(request):
    """Главная страница"""
    # Показываем последние 6 опубликованных зданий
    latest_buildings = HistoricalBuilding.objects.filter(status='published').order_by('-created_at')[:6]
    context = {
        'latest_buildings': latest_buildings,
    }
    return render(request, 'index.html', context)

# buildings/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import HistoricalBuilding, BuildingSuggestion
from .forms import BuildingSuggestionForm

def buildings_list(request):
    """Страница со списком всех зданий с фильтрацией по городам"""
    
    # Получаем параметр фильтра из URL
    city_filter = request.GET.get('city', 'all')
    
    # Базовый запрос (только опубликованные)
    buildings = HistoricalBuilding.objects.filter(status='published')
    
    # Применяем фильтр по городу
    if city_filter != 'all':
        buildings = buildings.filter(city=city_filter)
    
    # Сортируем по дате добавления (новые сверху)
    buildings = buildings.order_by('-created_at')
    
    # Пагинация (по 9 зданий на страницу)
    from django.core.paginator import Paginator
    paginator = Paginator(buildings, 9)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Собираем статистику по городам для отображения в фильтре
    city_stats = {
        'all': HistoricalBuilding.objects.filter(status='published').count(),
        'msk': HistoricalBuilding.objects.filter(status='published', city='msk').count(),
        'spb': HistoricalBuilding.objects.filter(status='published', city='spb').count(),
        'vlg': HistoricalBuilding.objects.filter(status='published', city='vlg').count(),
        'other': HistoricalBuilding.objects.filter(status='published', city='other').count(),
    }
    
    # Названия городов для отображения
    city_names = {
        'all': 'Все города',
        'msk': 'Москва',
        'spb': 'Санкт-Петербург',
        'vlg': 'Волгоград',
        'other': 'Другие города',
    }
    
    context = {
        'page_obj': page_obj,
        'total_count': buildings.count(),
        'current_city': city_filter,
        'city_stats': city_stats,
        'city_names': city_names,
    }
    return render(request, 'buildings.html', context)

def building_detail(request, building_id):
    """Детальная страница здания"""
    building = get_object_or_404(HistoricalBuilding, id=building_id, status='published')
    context = {
        'building': building,
    }
    return render(request, 'building_detail.html', context)

def about(request):
    """Страница 'О нас'"""
    return render(request, 'about.html')

def help_page(request):
    """Страница справки"""
    return render(request, 'help.html')

def suggest_building(request):
    """Предложить новое здание"""
    if request.method == 'POST':
        form = BuildingSuggestionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Спасибо! Ваше предложение отправлено на модерацию.')
            return redirect('index')
    else:
        form = BuildingSuggestionForm()
    
    context = {'form': form}
    return render(request, 'suggest_building.html', context)