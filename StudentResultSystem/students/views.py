from django.shortcuts import render, redirect
from .forms import (
    LoginForm,
    RegisterForm,
    StudentForm,
    ResultForm,
    SubjectForm,
    StudentAddForm,
)
from django.contrib.auth import login, logout, authenticate
from .models import Student, Result, Subject, User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.contrib import messages
from django.db.models import Q


def get_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B+"
    elif percentage >= 60:
        return "B"
    elif percentage >= 50:
        return "C"
    elif percentage >= 40:
        return "D"
    else:
        return "F"


def get_remarks(grade):
    remarks = {
        "A+": "Outstanding performance! Keep up the excellent work.",
        "A": "Very good performance. Continue with your dedication.",
        "B+": "Good work! With a bit more effort, you can achieve even better results.",
        "B": "Satisfactory performance. Focus on improving weak areas.",
        "C": "Average performance. Need to put in more consistent effort.",
        "D": "Just passing. Significant improvement needed in all subjects.",
        "F": "Failed. Please consult with your instructors and work harder.",
    }
    return remarks.get(grade, "")


def admin_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        raise PermissionDenied("You are not authorized to access this page.")

    return _wrapped_view


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            # Create User
            user = User(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
            )
            user.set_password(form.cleaned_data["password"])
            user.save()

            # Create Student profile
            Student.objects.create(
                user=user,
                name=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                phone=form.cleaned_data["phone"],
                address=form.cleaned_data["address"],
                profile_image=form.cleaned_data.get("profile_image"),
                is_approved=False,
            )

            login(request, user)
            if user.is_superuser:
                return redirect("dashboard")
            else:
                return redirect("student_profile")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                if user.is_superuser:
                    return redirect("dashboard")
                else:
                    try:
                        student = Student.objects.get(user=user)
                        if not student.is_approved:
                            return render(request, "pending_approval.html")
                    except Student.DoesNotExist:
                        return redirect("logout")
                    return redirect("student_profile")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def student_profile(request):
    try:
        student = Student.objects.get(user=request.user)
        if not student.is_approved:
            return render(request, "pending_approval.html")
    except Student.DoesNotExist:
        return redirect("logout")
    return render(request, "student_profile.html", {"student": student})


def student_list(request):
    query = request.GET.get("q")
    students = Student.objects.all().filter(is_approved=True)

    if query:
        students = students.filter(Q(name__icontains=query) | Q(email__icontains=query))

    paginator = Paginator(students, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "student_list.html",
        {"page_obj": page_obj, "query": query},
    )


@login_required
def my_results(request):
    try:
        student = Student.objects.get(user=request.user)
        if not student.is_approved:
            return render(request, "pending_approval.html")

        results = Result.objects.filter(student=student)

        for result in results:
            result.grade = get_grade(result.marks)  # type: ignore

        total_marks = sum(result.marks for result in results)
        num_subjects = len(results)
        max_possible = num_subjects * 100
        percentage = (total_marks / max_possible) * 100 if num_subjects > 0 else 0
        overall_grade = get_grade(percentage)
        remarks = get_remarks(overall_grade)

        context = {
            "student": student,
            "results": results,
            "total_marks": total_marks,
            "max_possible": max_possible,
            "percentage": percentage,
            "overall_grade": overall_grade,
            "remarks": remarks,
        }
        return render(request, "my_results.html", context)
    except Student.DoesNotExist:
        return render(request, "no_results.html")


@admin_required
def add_student(request):
    if request.method == "POST":
        form = StudentAddForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            try:
                student = Student.objects.get(user=user)
                student.is_approved = True
                student.save()
            except Student.DoesNotExist:
                pass
            return redirect("student_list")
    else:
        form = StudentAddForm()
    return render(request, "student_form.html", {"form": form})


@login_required
def update_student(request, id):
    student = Student.objects.get(pk=id)
    if not request.user.is_superuser and student.user != request.user:
        raise PermissionDenied("You are not allowed to update this student.")

    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            if request.user.is_superuser:
                return redirect("student_list")
            return redirect("student_profile")
    else:
        form = StudentForm(instance=student)

    return render(request, "student_form.html", {"form": form})


@admin_required
def delete_student(request, id):
    student = Student.objects.get(pk=id)
    student.delete()
    return redirect("student_list")


@login_required
def result_list(request):
    students = Student.objects.filter(
        results__isnull=False, is_approved=True
    ).distinct()
    student_data = {}

    for student in students:
        results = Result.objects.filter(student=student)

        total_marks = sum(result.marks for result in results)
        num_subjects = len(results)
        max_possible = num_subjects * 100
        percentage = (total_marks / max_possible) * 100 if num_subjects > 0 else 0
        overall_grade = get_grade(percentage)
        remarks = get_remarks(overall_grade)

        for result in results:
            result.grade = get_grade(result.marks)  # type: ignore

        student_data[student] = {
            "results": results,
            "total_marks": total_marks,
            "max_possible": max_possible,
            "percentage": percentage,
            "overall_grade": overall_grade,
            "remarks": remarks,
        }

    return render(request, "result_list.html", {"student_data": student_data})


@admin_required
def add_result(request):
    if request.method == "POST":
        form = ResultForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect("result_list")
            except IntegrityError:
                messages.error(
                    request, "This student already has a result for this subject."
                )
    else:
        form = ResultForm()
    return render(request, "result_form.html", {"form": form})


@admin_required
def update_result(request, id):
    result = Result.objects.get(pk=id)
    if request.method == "POST":
        form = ResultForm(request.POST, instance=result)
        if form.is_valid():
            form.save()
            return redirect("result_list")
    else:
        form = ResultForm(instance=result)
    return render(request, "result_form.html", {"form": form})


@admin_required
def delete_result(request, id):
    result = Result.objects.get(pk=id)
    result.delete()
    return redirect("result_list")


@admin_required
def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, "subject_list.html", {"subjects": subjects})


@admin_required
def add_subject(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("subject_list")
    else:
        form = SubjectForm()
    return render(request, "subject_form.html", {"form": form})


@admin_required
def update_subject(request, id):
    subject = Subject.objects.get(pk=id)
    if request.method == "POST":
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect("subject_list")
    else:
        form = SubjectForm(instance=subject)
    return render(request, "subject_form.html", {"form": form})


@admin_required
def delete_subject(request, id):
    subject = Subject.objects.get(pk=id)
    subject.delete()
    return redirect("subject_list")
