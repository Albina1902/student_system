from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.custom_login, name='custom_login'),
    path('cabinet/', views.cabinet, name='cabinet'),
    path('cabinet/student/', views.student_cabinet, name='student_cabinet'),
    path('cabinet/teacher/', views.teacher_cabinet, name='teacher_cabinet'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/accounts/login/'), name='logout_custom'),
]