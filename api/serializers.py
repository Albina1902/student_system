from rest_framework import serializers
from students.models import Student, Grade
from groups.models import Group
from courses.models import Course


class GroupSerializer(serializers.ModelSerializer):
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'name', 'faculty', 'student_count']

    def get_student_count(self, obj):
        return obj.students.count()


class CourseSerializer(serializers.ModelSerializer):
    teacher_name = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'teacher', 'teacher_name']

    def get_teacher_name(self, obj):
        if obj.teacher:
            return obj.teacher.get_full_name() or obj.teacher.username
        return None


class GradeSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Grade
        fields = ['id', 'student', 'student_name', 'course', 'course_title', 'value', 'date']


class StudentListSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.name', read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'email', 'group', 'group_name']


class StudentSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.name', read_only=True)
    grades = GradeSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'email', 'birth_date', 'group', 'group_name', 'grades']
