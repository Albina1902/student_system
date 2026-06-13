from django.contrib import admin
from django.urls import path, include
from .views import dashboard

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('admin/', admin.site.urls),

    # UI routes
    # UI routes
    path('students/', include('students.urls')),
    path('groups/', include('groups.urls')),
    path('courses/', include('courses.urls')),
    path('grades/', include('grades.urls')),        # ← добавить
    path('homework/', include('homework.urls')),    # ← добавить
    path('schedule/', include('schedule.urls')),    # ← добавить
    
    # API v1
    path('api/', include('api.urls')),

    # Auth
    path('accounts/', include('django.contrib.auth.urls')),
]