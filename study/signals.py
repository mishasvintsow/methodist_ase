from django.db.models.signals import post_save
from django.dispatch import receiver

import const
from als.models import ItemFeature
from .models import Module, ModuleHistory, Unit, Item, Test, switch_signal, clear_test_signal


@receiver(post_save, sender=Module)
def add_module(sender, instance, created, **kwargs):
    if created:
        ModuleHistory.objects.create(module=instance, switch='a' + instance.status)
        instance.save()


@receiver(switch_signal, sender=Module)
def switch_status(sender, instance, old, new, **kwargs):
    ModuleHistory.objects.create(module=instance, switch=old + new)


@receiver(clear_test_signal, sender=Test)
def clear_test(sender, test, **kwargs):
    Item.objects.filter(unit__test=test, status=const.ITEM_STATUS_NORESPONSE).delete()
