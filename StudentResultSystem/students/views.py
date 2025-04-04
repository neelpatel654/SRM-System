from django.shortcuts import render,redirect
from .forms import LoginForm, RegisterForm, StudentForm, ResultForm, SubjectForm
from django.contrib.auth import login,logout,authenticate
from .models import Student, Result, Subject
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q



def admin_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        raise PermissionDenied("You are not authorized to access this page.")
    return _wrapped_view


def register_view(request):
    if request.method=='POST':
        form = RegisterForm(request.POST)
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()

        Student.objects.create(
                user=user,
                name=user.username,
                email=user.email,
                phone='',
                address=''
            )

        login(request, user)
        return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request,'register.html',{'form':form})

def login_view(request):
    if request.method=='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user:
                login(request,user)
                return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request,'login.html',{'form':form})

def logout_view(request):
    logout(request)
    return redirect('login')


def student_list(request):
    query = request.GET.get('q')
    students = Student.objects.all()

    if query:
        students = students.filter(
            Q(name__icontains=query) | Q(email__icontains=query)
        )

    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'student_list.html', {
        'page_obj': page_obj,
        'query': query,
    })

@login_required
def my_results(request):
    try:
        student = Student.objects.get(email=request.user.email)
    except Student.DoesNotExist:
        return render(request, 'no_results.html')

    results = Result.objects.filter(student=student)
    return render(request, 'my_results.html', {'results': results})



@admin_required
def add_student(request):
    if request.method=="POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request,'student_form.html',{'form':form})

@admin_required
def update_student(request, id):
    student = Student.objects.get(pk=id)
    if request.method=='POST':
        form = StudentForm(request.POST,instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request,'student_form.html',{'form':form})

@admin_required
def delete_student(request, id):
    student = Student.objects.get(pk=id)
    student.delete()
    return redirect('student_list')


@login_required
def result_list(request):
    results = Result.objects.all()
    return render(request,'result_list.html',{'results':results})

@admin_required
def add_result(request):
    if request.method=="POST":
        form = ResultForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('result_list')
    else:
        form = ResultForm()
    return render(request,'result_form.html',{'form':form})


@admin_required
def update_result(request,id):
    result = Result.objects.get(pk=id)
    if request.method=="POST":
        form = ResultForm(request.POST,instance=result)
        if form.is_valid():
            form.save()
            return redirect('result_list')
    else:
        form = ResultForm(instance=result)
    return render(request,'result_form.html',{'form':form})

@admin_required
def delete_result(request,id):
    result = Result.objects.get(pk=id)
    result.delete()
    return redirect('result_list')


@admin_required
def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'subject_list.html', {'subjects': subjects})

@admin_required
def add_subject(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subject_list')
    else:
        form = SubjectForm()
    return render(request, 'subject_form.html', {'form': form})

@admin_required
def update_subject(request, id):
    subject = Subject.objects.get(pk=id)
    if request.method == "POST":
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('subject_list')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'subject_form.html', {'form': form})

@admin_required
def delete_subject(request, id):
    subject = Subject.objects.get(pk=id)
    subject.delete()
    return redirect('subject_list')