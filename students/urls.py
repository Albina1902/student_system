from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('create/', views.student_create, name='student_create'),
    path('<int:pk>/', views.student_detail, name='student_detail'),
    path('<int:pk>/edit/', views.student_update, name='student_update'),
    path('<int:pk>/delete/', views.student_delete, name='student_delete'),
    path('grade/create/', views.grade_create, name='grade_create'),
    path('register/', views.register_student, name='student_register'),
    path('qr-code/', views.qr_code_view, name='student_qr_code'),
]