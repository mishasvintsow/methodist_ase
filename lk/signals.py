# Signals
from django.db.models import Max
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Student, Teacher


@receiver(post_save, sender=User)
def handler_create_student_or_teacher(sender, instance, created, **kwargs):
    if created and instance.is_student():
        Student.objects.create(user=instance, SID=Student.objects.aggregate(max_SID=Max('SID'))['max_SID'] + 1)
    elif created and instance.is_moderator():
        Teacher.objects.create(user=instance, PID=Teacher.objects.aggregate(max_PID=Max('PID'))['max_PID'] + 1)
