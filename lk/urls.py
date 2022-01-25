from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import RegistrationView, ProfileDetailView, MyProfileDetailView, StudentUpdateView, UsersListView, \
    StudentsListView, TeachersListView, BecomeStudentView, MyProfileUpdateView, \
    ProfileUpdateView, IndexView, CustomPasswordResetView

urlpatterns = [
    path('', IndexView.as_view(), name='/'),
    path('lk/login/', LoginView.as_view(template_name='lk/login.html'), name='login'),
    path('lk/logout/', LogoutView.as_view(template_name='lk/logout.html'), name='logout'),
    path('lk/reg/', RegistrationView.as_view(), name='reg'),
    path('lk/profile/', MyProfileDetailView.as_view(), name='profile_detail'),
    path('lk/profile/edit', MyProfileUpdateView.as_view(), name='profile_update'),
    path('lk/profile/change-password/', CustomPasswordResetView.as_view(), name='reset_password'),
    path('users/', UsersListView.as_view(), name='users_list'),
    path('users/<int:pk>', ProfileDetailView.as_view(), name='profile_detail'),
    path('users/<int:pk>/edit', ProfileUpdateView.as_view(), name='profile_update'),
    path('users/<int:pk>/change-password/', CustomPasswordResetView.as_view(), name='reset_password'),
    path('students/', StudentsListView.as_view(), name='students_list'),
    path('students/<int:SID>/profile/edit', StudentUpdateView.as_view(), name='student_update'),
    path('teachers/', TeachersListView.as_view(), name='teachers_list'),
    path('lk/profile/becomestudent/', BecomeStudentView.as_view(), name='become_student'),
]
