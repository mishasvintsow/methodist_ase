from django.db.models.signals import post_save
from django.dispatch import receiver

import const
from lk.models import Student
from domain.models import Topic, Task
from study.models import Module, Test, Unit, Item
from .models import StudentFeature, TopicFeature, TaskFeature, ModuleFeature, TestFeature, UnitFeature, ItemFeature, \
    StudentParam, ModuleParam, UnitParam


@receiver(post_save, sender=Student)
def add_student(sender, instance, created, **kwargs):
    if created:
        StudentFeature.objects.create(student=instance).refresh_features()
        StudentParam.objects.create(student=instance).refresh_params()


@receiver(post_save, sender=Topic)
def add_topic(sender, instance, created, **kwargs):
    if created:
        TopicFeature.objects.create(topic=instance).refresh_features()


@receiver(post_save, sender=Task)
def add_task(sender, instance, created, **kwargs):
    if created:
        TaskFeature.objects.create(task=instance).refresh_features()


@receiver(post_save, sender=Module)
def add_module(sender, instance, created, **kwargs):
    if created:
        ModuleFeature.objects.create(module=instance).refresh_features()
        ModuleParam.objects.create(module=instance).refresh_params()


@receiver(post_save, sender=Test)
def add_test(sender, instance, created, **kwargs):
    if created:
        TestFeature.objects.create(test=instance).refresh_features()


@receiver(post_save, sender=Unit)
def add_unit(sender, instance, created, **kwargs):
    if created:
        UnitFeature.objects.create(unit=instance).refresh_features()
        UnitParam.objects.create(unit=instance).refresh_params()


@receiver(post_save, sender=Item)
def add_item(sender, instance, created, **kwargs):
    if created:
        ItemFeature.objects.create(item=instance,
                                   **instance.unit.get_features(),
                                   **instance.task.get_features())
