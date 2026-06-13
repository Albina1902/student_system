from django.shortcuts import render, redirect, get_object_or_404
from .models import Course
from .forms import CourseForm


# ---------- LIST ----------
def course_list(request):
    courses = Course.objects.all()
    return render(request, "courses/course_list.html", {
        "courses": courses
    })


# ---------- CREATE ----------
def course_create(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("course_list")
    else:
        form = CourseForm()

    return render(request, "courses/course_form.html", {
        "form": form
    })


# ---------- UPDATE ----------
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect("course_list")
    else:
        form = CourseForm(instance=course)

    return render(request, "courses/course_form.html", {
        "form": form
    })


# ---------- DELETE ----------
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == "POST":
        course.delete()
        return redirect("course_list")

    return render(request, "courses/course_confirm_delete.html", {
        "course": course
    })