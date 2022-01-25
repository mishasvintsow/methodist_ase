from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple

import const
from .models import User, Student, Teacher


class UserAddForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('role', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(UserAddForm, self).__init__(*args, **kwargs)
        self.fields['role'].choices = const.PROFILE_ROLES_DISPLAY[1:]
        self.fields['role'].widget.choices = const.PROFILE_ROLES_DISPLAY[1:]


class UserResetPasswordForm(ModelForm):
    class Meta:
        model = User
        fields = ['password']


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class StudentUpdateForm(ModelForm):
    class Meta:
        model = Student
        fields = ['user', 'SID', 'grade', 'pause', 'teacher']

    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget.attrs.update({'readonly': True})
        self.fields['SID'].widget.attrs.update({'readonly': True})


class TeacherStudentsUpdateForm(ModelForm):
    class Meta:
        model = Teacher
        fields = []

    students = ModelMultipleChoiceField(
        queryset=User.objects.filter(role=const.PROFILE_ROLE_STUDENT),
        widget=CheckboxSelectMultiple
    )
