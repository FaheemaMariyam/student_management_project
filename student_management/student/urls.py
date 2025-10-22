from django.urls import path
from . import views
urlpatterns=[
    path('',views.home,name='home'),
    path('login/',views.login_user,name='login'),
    path('register/',views.register_user,name='register'),
    path('logout/',views.logout_user,name='logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('profile/',views.student_profile_view,name='profile'),
    path('profile/edit',views.student_profile_edit,name='profile_edit'),
    path('dashboard/students',views.students_list,name='students_list'),
    path('dashboard/add',views.add_students,name='add_students'),
    path('dashboard/students/edit/<int:pk>/',views.edit_students,name='edit_students'),
    path('dashboard/students/delete/<int:pk>/',views.delete_students,name='delete_students')
]

