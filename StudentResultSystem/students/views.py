from django.shortcuts import render,redirect
from .forms import LoginForm, RegisterForm, StudentForm, ResultForm
from django.contrib.auth import login,logout,authenticate
from .models import Student, Result
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method=='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
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

@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request,'student_list.html',{'students':students})

@login_required
def add_student(request):
    if request.method=="POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request,'student_form.html',{'form':form})

@login_required
def update_student(request, id):
    student = Student.objects.get(pk=id)
    if request.method=='POST':
        form = StudentForm(request.POST,instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request,'student_from.html',{'form':form})

@login_required
def delete_student(request, id):
    student = Student.objects.get(pk=id)
    student.delete()
    return redirect('student_list')


@login_required
def result_list(request):
    results = Result.objects.all()
    return render(request,'result_list.html',{'results':results})

@login_required
def add_result(request):
    if request.method=="POST":
        form = ResultForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('result_list')
    else:
        form = ResultForm()
    return render(request,'result_form.html',{'form':form})


@login_required
def update_result(request,id):
    result = Result.objects.get(pk=id)
    if request.method=="POST":
        form = ResultForm(request.POST,instance=result)
        if form.is_valid():
            form.save()
            return redirect('result_list')
    else:
        form = ResultForm()
    return render(request,'result_form.html',{'form':form})

@login_required
def delete_result(request,id):
    result = Result.objects.get(pk=id)
    result.delete()
    return redirect('result_list')