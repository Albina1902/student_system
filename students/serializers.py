from rest_framework import serializers
from students.models import Student, Grade
from groups.models import Group
from courses.models import Course


# ─── Group ────────────────────────────────────────────────────────────────────

class GroupSerializer(serializers.ModelSerializer):
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'name', 'faculty', 'student_count', 'created_at']

    def get_student_count(self, obj):
        return obj.students.count()


# ─── Course ───────────────────────────────────────────────────────────────────

class CourseSerializer(serializers.ModelSerializer):
    teacher_name = serializers.SerializerMethodField()
    average_grade = serializers.SerializerMethodField()
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description',
            'teacher', 'teacher_name',
            'groups', 'average_grade', 'student_count',
            'created_at'
        ]

    def get_teacher_name(self, obj):
        if obj.teacher:
            return obj.teacher.get_full_name() or obj.teacher.username
        return None

    def get_average_grade(self, obj):
        return obj.average_grade()

    def get_student_count(self, obj):
        return obj.student_count()


# ─── Grade ────────────────────────────────────────────────────────────────────

class GradeSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Grade
        fields = ['id', 'student', 'student_name', 'course', 'course_title', 'value', 'date']


# ─── Student ──────────────────────────────────────────────────────────────────

class StudentSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.name', read_only=True)
    faculty = serializers.CharField(source='group.faculty', read_only=True)
    average_grade = serializers.SerializerMethodField()
    grades = GradeSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = [
            'id', 'first_name', 'last_name', 'full_name',
            'email', 'birth_date',
            'group', 'group_name', 'faculty',
            'average_grade', 'grades'
        ]

    def get_average_grade(self, obj):
        return obj.average_grade()


class StudentListSerializer(serializers.ModelSerializer):
    """Лёгкий сериализатор для списков (без вложенных grades)"""
    group_name = serializers.CharField(source='group.name', read_only=True)
    average_grade = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'email', 'group', 'group_name', 'average_grade']

    def get_average_grade(self, obj):
        return obj.average_grade()