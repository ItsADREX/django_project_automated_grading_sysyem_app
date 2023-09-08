from django.shortcuts import render, redirect
from .forms import InstructorLoginForm, StudentLoginForm, StudentRegistrationForm, InstructorRegistrationForm

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'STUDENT'
            user.save()
            return redirect('login_student')
           
    else:
        form = StudentRegistrationForm()
    return render(request, 'AccountsApp/register_student.html', {'form': form})

def register_instructor(request):
    if request.method == 'POST':
        form = InstructorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'INSTRUCTOR'
            user.save()
            print("User saved")
            return redirect('login_instructor')
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = InstructorRegistrationForm()
    return render(request, 'AccountsApp/register_instructor.html', {'form': form})



from django.contrib.auth import login, authenticate

def login_student(request):
    if request.method == 'POST':
        form = StudentLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('student_dashboard')
    else:
        form = StudentLoginForm()
    return render(request, 'AccountsApp/login_student.html', {'form': form})

def login_instructor(request):
    if request.method == 'POST':
        form = InstructorLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('instructor_dashboard')
    else:
        form = InstructorLoginForm()
    return render(request, 'AccountsApp/login_instructor.html', {'form': form})

