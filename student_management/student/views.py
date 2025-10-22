from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from .forms import UserRegisterForm
from .forms import StudentProfileForm
from .models import StudentProfile
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from datetime import date
from .forms import AdminStudentProfileForm

from .forms import AdminStudentEditForm
def home(request):
    return render(request,'home.html')
def register_user(request):
    if request.method=='POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,f"Registation successfull,you can login now")
            return redirect('login')
    else:
        form=UserRegisterForm()
    return render(request,'register.html',{'form':form})
def login_user(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
        
    return render(request,'login.html')
@login_required
def logout_user(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')
@login_required
def dashboard(request):
    user=request.user
    if user.is_superuser or user.role=='Admin':
        return render(request,'admin_dashboard.html',{'user':user})
    elif user.role=='Student':
        return render(request,'student_dashboard.html',{'user':user})
    else:
        return HttpResponse("Role not specified")
@login_required
def student_profile_view(request):
    profile,created=StudentProfile.objects.get_or_create(user=request.user)
    return render(request,'student_profile_view.html',{'profile':profile})
@login_required
def student_profile_edit(request):
    profile,created=StudentProfile.objects.get_or_create(user=request.user)
    if request.method=='POST':
        form=StudentProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            student=form.save(commit=False)
            #calculate age from dob
            if student.date_of_birth:
                today=date.today()
                age=today.year - student.date_of_birth.year
                if (today.month,today.day)<(student.date_of_birth.month,student.date_of_birth.day):
                    age-=1
                student.age=age
            student.save()
            return redirect('profile')
    else:
        form=StudentProfileForm(instance=profile)
    return render(request,'student_profile_edit.html',{'form':form})
@staff_member_required
def students_list(request):
    
        # students=StudentProfile.objects.filter(user__role='Student',
        #                                        student_name__istartswith='r'
        #                                        )
        students=StudentProfile.objects.filter(user__role='Student')
   
        return render(request,'students_list.html',{'students':students})
@staff_member_required
def add_students(request):
    if request.method=='POST':
        user_form=UserRegisterForm(request.POST)#this used bcz it is not null column,so admin add the username,and password
        profile_form=AdminStudentProfileForm(request.POST,request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
             # for Create the user first
            user = user_form.save(commit=False)
            user.role = 'Student'
            user.save()
             # Create student profile and link the user
            student = profile_form.save(commit=False)
            student.user = user
            student.save()
            if student.date_of_birth:
                today=date.today()
                age=today.year - student.date_of_birth.year
                if (today.month,today.day)<(student.date_of_birth.month,student.date_of_birth.day):
                    age-=1
                student.age=age
            student.save()
            messages.success(request,f"{student.student_name} added successfully ")
            return redirect('students_list')
    else:
        user_form=AdminStudentEditForm(instance=student.user)
        profile_form=AdminStudentProfileForm()
    return render(request,'add_students.html',{'user_form': user_form, 'profile_form': profile_form})
@staff_member_required
def edit_students(request, pk):
    students_qset = StudentProfile.objects.filter(pk=pk)
    if not students_qset.exists():
        messages.error(request, "Student not found")
        return redirect('students_list')

    student = students_qset.first()
    
    if request.method == 'POST':
        user_form = AdminStudentEditForm(request.POST, instance=student.user)
        profile_form = AdminStudentProfileForm(request.POST, request.FILES, instance=student)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            student = profile_form.save(commit=False)

            if student.date_of_birth:
                today = date.today()
                age = today.year - student.date_of_birth.year
                if (today.month, today.day) < (student.date_of_birth.month, student.date_of_birth.day):
                    age -= 1
                student.age = age

            student.save()
            messages.success(request, f"{student.student_name} updated successfully")
            return redirect('students_list')
    else:
        user_form = AdminStudentEditForm(instance=student.user)
        profile_form = AdminStudentProfileForm(instance=student)

    return render(request, 'edit_students.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
@staff_member_required
def delete_students(request,pk):
    students_qset=StudentProfile.objects.filter(pk=pk)
    if not students_qset.exists():
        messages.error(request,f"student not found")
        return redirect('students_list')
    student=students_qset.first()
    user=student.user
    student.delete()
    user.delete()
    messages.success(request,f"{student.student_name} has been deleted successfully")
    return redirect('students_list')