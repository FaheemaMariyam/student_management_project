from django import forms
from django.contrib.auth.forms  import UserCreationForm
from .models import User
from .models import StudentProfile
from datetime import date
class UserRegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        #this is for save the role as student
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'Student'  # default role for all registered users
        if commit:
            user.save()
        return user
class StudentProfileForm(forms.ModelForm):
    class Meta:
        model=StudentProfile
        fields=['student_name', 'phone', 'address' ,'date_of_birth', 'profile_image']
        #for date picker
        widgets = {
            'student_enrollment_date': forms.DateInput(attrs={'type': 'date'}),
            'date_of_birth': forms.DateInput(
                attrs={
                    'type': 'date',
                    'max': date.today().strftime('%Y-%m-%d')  # Prevent future dates
                }
            ),
        }
class AdminStudentProfileForm(forms.ModelForm):
    class Meta:
        model=StudentProfile
        fields=[
            
            'student_name','student_rollno','student_course',
            'student_enrollment_date','phone','address',
            'date_of_birth','age','profile_image'
        ]
        widgets={
            'student_enrollment_date': forms.DateInput(attrs={'type': 'date'}),
            'date_of_birth': forms.DateInput(
                attrs={
                    'type': 'date',
                    'max': date.today().strftime('%Y-%m-%d')  
                }
            ),
        }
class AdminStudentEditForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email']