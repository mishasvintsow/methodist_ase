from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Count, Q, Case, When, Value, IntegerField, F, CharField
from django.utils import timezone

import const


class User(AbstractUser):
    role = models.CharField(max_length=1, choices=const.PROFILE_ROLES_DISPLAY, default=const.PROFILE_ROLE_ANON,
                            verbose_name="Роль пользователя")

    def is_root(self):
        return self.role == const.PROFILE_ROLE_ROOT

    def is_methodist(self):
        return self.role == const.PROFILE_ROLE_METHODIST

    def is_auditor(self):
        return self.role == const.PROFILE_ROLE_AUDITOR

    def is_teacher(self):
        return self.role == const.PROFILE_ROLE_TEACHER

    def is_student(self):
        return self.role == const.PROFILE_ROLE_STUDENT

    def is_admin(self):
        return const.PROFILE_ROLES_ADMIN.find(self.role) != -1

    def is_moderator(self):
        return const.PROFILE_ROLES_MODERATOR.find(self.role) != -1

    def has_student_obj(self):
        return hasattr(self, 'student')

    def get_role_name(self):
        return const.PROFILE_ROLES[self.role]

    def set_role(self, r):
        if const.PROFILE_ROLES_ALL.find(r) != -1:
            self.role = r
        else:
            self.role = const.PROFILE_ROLE_ANON
        self.save()


class StudentManager(models.Manager):
    def get_annotated_qs(self):
        qs = self.all()
        qs = Student.objects.annotate(homework_count=Count('tests', distinct=True, filter=Q(
            tests__time_open__range=[timezone.now() - timedelta(days=7), timezone.now()], tests__practice=False)))
        qs = qs.annotate(homework_filter=Case(When(homework_count__gt=0, then=Value('1')),
                                              default=Value('0'),
                                              output_field=CharField()))
        qs = qs.annotate(analysis_week=Count('tests__test_units__unit_items__IID', distinct=True, filter=Q(
            tests__test_units__unit_items__analysis=const.ITEM_ANALYSIS_TODO) & Q(
            tests__test_units__unit_items__time_finish__range=[timezone.now() - timedelta(days=7), timezone.now()])))
        qs = qs.annotate(analysis_more=Count('tests__test_units__unit_items__IID', distinct=True, filter=Q(
            tests__test_units__unit_items__analysis=const.ITEM_ANALYSIS_TODO) & Q(
            tests__test_units__unit_items__time_finish__lt=timezone.now() - timedelta(days=7))))
        qs = qs.annotate(analysis_filter=Case(When(analysis_more__gt=0, then=Value('1')),
                                              When(analysis_week__gt=0, then=Value('2')),
                                              default=Value('0'),
                                              output_field=CharField()))
        qs = qs.annotate(count_high_regress=Count('modules__MID', distinct=True,
                                                  filter=Q(modules__moduleparam__color=const.MODULE_COLOR_RED)))
        qs = qs.annotate(count_low_regress=Count('modules__MID', distinct=True,
                                                 filter=Q(modules__moduleparam__color=const.MODULE_COLOR_PINK)))
        qs = qs.annotate(
            regress_filter=Case(When(Q(count_low_regress__gt=0) & Q(count_high_regress__gt=0), then=Value('1')),
                                When(Q(count_low_regress__gt=0), then=Value('2')),
                                When(Q(count_high_regress__gt=0), then=Value('3')),
                                default=Value('0'),
                                output_field=CharField()))
        qs = qs.annotate(
            learning_count=Count('modules__MID', distinct=True, filter=Q(modules__moduleparam__LPRT__isnull=False,
                                                                         modules__moduleparam__LPRT__lt=F(
                                                                             'studentparam__MRPRT'))))
        qs = qs.annotate(learning_filter=Case(When(learning_count__gt=0, then=Value('1')),
                                              default=Value('0'),
                                              output_field=CharField()))
        return qs


class Student(models.Model):
    class Meta:
        ordering = ['SID']

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='student')
    SID = models.IntegerField(unique=True, null=True)
    grade = models.IntegerField(choices=const.GRADES_DISPLAY, default=const.GRADES[0], verbose_name="Класс")
    pause = models.BooleanField(default=False, verbose_name="Пауза")
    teacher = models.ForeignKey('Teacher',
                                on_delete=models.CASCADE,
                                related_name='students',
                                null=True,
                                blank=True,
                                verbose_name="Преподаватель")
    old = models.BooleanField(default=False)

    objects = StudentManager()

    def check_tests(self):
        from study.models import Test
        tests = Test.objects.filter(student=self)
        for test in tests:
            test.check_status()


class Teacher(models.Model):
    class Meta:
        ordering = ['PID']

    PID = models.IntegerField(unique=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                limit_choices_to={'role__exact': const.PROFILE_ROLE_TEACHER, }, )

    def __str__(self):
        return "Преподаватель: " + self.user.get_full_name()
