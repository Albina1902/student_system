from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters
from students.models import Student, Grade
from groups.models import Group
from courses.models import Course
from .serializers import (
    StudentSerializer, StudentListSerializer,
    GroupSerializer, CourseSerializer, GradeSerializer
)


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.select_related('group').prefetch_related('grades')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['last_name', 'first_name']

    def get_serializer_class(self):
        if self.action == 'list':
            return StudentListSerializer
        return StudentSerializer

    @action(detail=True, methods=['get'], url_path='grades')
    def grades(self, request, pk=None):
        student = self.get_object()
        grades = student.grades.select_related('course')
        return Response(GradeSerializer(grades, many=True).data)


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    @action(detail=True, methods=['get'], url_path='students')
    def students(self, request, pk=None):
        students = self.get_object().students.all()
        return Response(StudentListSerializer(students, many=True).data)


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.select_related('teacher')
    serializer_class = CourseSerializer


class GradeViewSet(ModelViewSet):
    queryset = Grade.objects.select_related('student', 'course')
    serializer_class = GradeSerializer
