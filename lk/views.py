from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.http import HttpResponseNotFound
from django.shortcuts import reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

import const
from mixins import UserPermissionsMixin
from .filters import StudentsFilter
from .forms import UserAddForm, StudentUpdateForm, TeacherStudentsUpdateForm, UserResetPasswordForm
from .models import User, Student, Teacher


class IndexView(LoginRequiredMixin, UserPermissionsMixin, RedirectView):
    access = const.PROFILE_ROLES_ALL

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        if user.is_admin():
            return reverse_lazy('users_list')
        elif user.is_teacher():
            return reverse_lazy('students_list')
        elif user.is_auditor():
            return reverse_lazy('moderation_tasks_list')
        elif user.is_student():
            return reverse_lazy('student_tests_list')
        else:
            return HttpResponseNotFound('<h1>Page not found</h1>')


class RegistrationView(LoginRequiredMixin, UserPermissionsMixin, CreateView):
    access = const.PROFILE_ROLES_ADMIN
    template_name = "lk/reg.html"
    form_class = UserAddForm

    def get_success_url(self):
        if self.object.is_student():
            return reverse('student_update', kwargs={'SID': self.object.student.SID})
        else:
            return reverse('profile_detail', kwargs={'pk': self.object.pk})


class ProfileDetailView(LoginRequiredMixin, UserPermissionsMixin, DetailView):
    access = const.PROFILE_ROLES_ADMIN
    model = User
    template_name = "lk/profile_detail.html"
    context_object_name = 'user'

    def get_object(self, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return user


class ProfileUpdateView(LoginRequiredMixin, UserPermissionsMixin, UpdateView):
    access = const.PROFILE_ROLES_ADMIN
    model = User
    template_name = "lk/profile_update.html"
    context_object_name = 'user'
    fields = ['username', 'first_name', 'last_name', 'email', 'role']

    def get_object(self, **kwargs):
        return get_object_or_404(User, pk=self.kwargs['pk'])

    def get_success_url(self, **kwargs):
        return reverse_lazy("profile_detail", args=(self.object.pk,))


class CustomPasswordResetView(LoginRequiredMixin, UserPermissionsMixin, UpdateView):
    access = const.PROFILE_ROLES_ADMIN
    model = User
    template_name = "lk/reset_password.html"
    context_object_name = 'user'
    form_class = SetPasswordForm

    def get_object(self, **kwargs):
        if 'pk' in self.kwargs:
            return get_object_or_404(User, pk=self.kwargs['pk'])
        else:
            return self.request.user

    def get_form_kwargs(self):
        kwargs = super(CustomPasswordResetView, self).get_form_kwargs()
        kwargs['user'] = self.get_object()
        kwargs.pop('instance', None)
        return kwargs

    def get_success_url(self, **kwargs):
        self.success_url = self.request.META.get('HTTP_REFERER', '/')
        return self.success_url


class MyProfileDetailView(LoginRequiredMixin, TemplateView):
    template_name = "lk/profile_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class MyProfileUpdateView(LoginRequiredMixin, UserPermissionsMixin, UpdateView):
    access = const.PROFILE_ROLES_MODERATOR
    model = User
    template_name = "lk/profile_update.html"
    context_object_name = 'user'
    fields = ['username', 'first_name', 'last_name', 'email', 'role']

    def get_object(self, **kwargs):
        return self.request.user

    def get_success_url(self, **kwargs):
        return reverse_lazy("profile_detail", args=(self.object.pk,))


class StudentUpdateView(LoginRequiredMixin, UserPermissionsMixin, UpdateView):
    access = const.PROFILE_ROLES_ADMIN
    template_name = 'lk/student_update.html'
    model = Student
    form_class = StudentUpdateForm
    context_object_name = 'student'

    def get_object(self, **kwargs):
        return Student.objects.get(SID=self.kwargs['SID'])

    def get_success_url(self):
        return reverse('profile_detail', kwargs={'pk': self.object.user.pk})


class UsersListView(LoginRequiredMixin, UserPermissionsMixin, ListView):
    access = const.PROFILE_ROLES_ADMIN
    model = User
    template_name = "lk/users_list.html"
    context_object_name = 'users'


class StudentsListView(LoginRequiredMixin, UserPermissionsMixin, ListView):
    access = const.PROFILE_ROLES_MODERATOR
    model = Student
    template_name = "lk/students_list.html"
    context_object_name = 'students'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StudentsListView, self).get_context_data()
        qs = Student.objects.get_annotated_qs()
        if self.request.user.is_teacher():
            qs = qs.filter(teacher=self.request.user.teacher)
        filter_ = StudentsFilter(self.request.GET, queryset=qs)
        context['filter'] = filter_
        context['students'] = filter_.qs
        return context


class TeachersListView(LoginRequiredMixin, UserPermissionsMixin, ListView):
    access = const.PROFILE_ROLES_ADMIN
    model = Teacher
    template_name = "lk/teachers_list.html"
    context_object_name = 'teachers'


class BecomeStudentView(LoginRequiredMixin, UserPermissionsMixin, RedirectView):
    access = const.PROFILE_ROLES_ADMIN

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        student, _ = Student.objects.get_or_create(user=user,
                                                   defaults={
                                                       'SID': max(Student.objects.all().values_list('SID', flat=True),
                                                                  default=0) + 1})

        return reverse_lazy('student_update', args=(student.SID,))
