from django.core.exceptions import PermissionDenied

from lk.models import Student


class UserPermissionsMixin(object):

    def has_permissions(self):
        return self.request.user.role in self.access

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise PermissionDenied()
        return super(UserPermissionsMixin, self).dispatch(request, *args, **kwargs)


class StudentPermissionsMixin(object):

    def has_permissions(self):
        return Student.objects.filter(user=self.request.user).exists()

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise PermissionDenied()
        return super(StudentPermissionsMixin, self).dispatch(request, *args, **kwargs)
