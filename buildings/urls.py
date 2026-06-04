from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('buildings/', views.buildings_list, name='buildings_list'),
    path('building/<int:building_id>/', views.building_detail, name='building_detail'),
    path('about/', views.about, name='about'),
    path('help/', views.help_page, name='help'),
    path('suggest/', views.suggest_building, name='suggest_building'),
]