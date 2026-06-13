from django.urls import path
from . import views

urlpatterns = [
    path('', views.homework_list, name='homework_list'),
    path('add/', views.homework_create, name='homework_create'),
    path('<int:pk>/', views.homework_detail, name='homework_detail'),
    path('<int:pk>/edit/', views.homework_edit, name='homework_edit'),
    path('<int:pk>/delete/', views.homework_delete, name='homework_delete'),
    path('<int:pk>/ai/', views.ai_explain, name='homework_ai_explain'),
]
