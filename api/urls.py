from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, GroupViewSet, CourseViewSet, GradeViewSet

router = DefaultRouter()
router.register('students', StudentViewSet, basename='student')
router.register('groups', GroupViewSet, basename='group')
router.register('courses', CourseViewSet, basename='course')
router.register('grades', GradeViewSet, basename='grade')

urlpatterns = router.urls
