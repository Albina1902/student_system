from django.shortcuts import render
from django.db.models import Count, Avg

from students.models import Student, Grade
from groups.models import Group
from courses.models import Course


def dashboard(request):
    total_students = Student.objects.count()
    total_groups = Group.objects.count()
    total_courses = Course.objects.count()

    # Average grade
    average_grade = Grade.objects.aggregate(
        avg=Avg("value")
    )["avg"] or 0

    # Groups analytics
    groups = Group.objects.annotate(
        student_count=Count("students")
    )

    group_labels = list(groups.values_list("name", flat=True))
    group_counts = list(groups.values_list("student_count", flat=True))

    # Courses analytics (⚠ поле названия может отличаться)
    courses = Course.objects.annotate(
        avg_grade=Avg("grades__value")
    )

    # ⭐ IMPORTANT — проверь поле названия курса
    # Если у тебя не "name", измени здесь
    course_labels = list(courses.values_list("id", flat=True))
    course_averages = [
        round(c.avg_grade, 2) if c.avg_grade else 0
        for c in courses
    ]

    context = {
        "total_students": total_students,
        "total_groups": total_groups,
        "total_courses": total_courses,
        "average_grade": round(average_grade, 2),

        "group_labels": group_labels,
        "group_counts": group_counts,

        "course_labels": course_labels,
        "course_averages": course_averages,
    }

    return render(request, "dashboard.html", context)