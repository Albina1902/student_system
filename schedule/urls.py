from django.urls import path
from . import views

urlpatterns = [
    path('', views.schedule_list, name='schedule_list'),
    path('add/', views.schedule_create, name='schedule_create'),
    path('<int:pk>/edit/', views.schedule_edit, name='schedule_edit'),
    path('<int:pk>/delete/', views.schedule_delete, name='schedule_delete'),
]
