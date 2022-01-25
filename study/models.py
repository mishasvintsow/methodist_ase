from datetime import timedelta

from django.db import models
from django.db.models import Max
from django.dispatch import Signal
from django.utils import timezone

import const
from domain.models import Task
from lk.models import Student

switch_signal = Signal(providing_args=["instance", "old", "new"])
clear_test_signal = Signal(providing_args=["test"])


class Module(models.Model):
    class Meta:
        ordering = ['student__SID', 'order']

    MID = models.IntegerField(unique=True)
    student = models.ForeignKey(Student,
                                on_delete=models.CASCADE,
                                related_name='modules')
    topic = models.ForeignKey('domain.Topic', on_delete=models.CASCADE)
    status = models.CharField(max_length=1,
                              choices=const.MODULE_STATUSES_DISPLAY,
                              default=const.MODULE_STATUS_IRRELEVANT)
    order = models.IntegerField(null=True)

    def __str__(self):
        return "%s - %s" % (self.get_status_display(), str(self.topic))

    def set_status(self, new):
        switch_signal.send(sender=self.__class__, instance=self, old=self.status, new=new)
        self.status = new
        self.save()

    def delete(self, *args, **kwargs):
        switch_signal.send(sender=self.__class__, instance=self, old=self.status, new=const.MODULE_STATUS_DELETED)
        self.status = const.MODULE_STATUS_DELETED
        self.save()


class ModuleHistoryManager(models.Manager):
    def get_last_change(self, module):
        return super(ModuleHistoryManager, self).get_queryset().filter(module=module).order_by('-timestamp').first()


class ModuleHistory(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    switch = models.CharField(max_length=2, choices=const.MODULE_STATUSES_SWITCH_DISPLAY,
                              default=const.MODULE_STATUS_ADD_IRRELEVANT, help_text='Switch status of module')
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ModuleHistoryManager()

    def get_last_status(self):
        return self.switch[1]


class Test(models.Model):
    class Meta:
        ordering = ['TID']

    TID = models.IntegerField(unique=True)
    student = models.ForeignKey(Student,
                                on_delete=models.CASCADE,
                                related_name='tests')
    status = models.CharField(max_length=1,
                              choices=const.TEST_STATUSES_DISPLAY,
                              default=const.TEST_STATUS_CREATED)
    time_create = models.DateTimeField(auto_now_add=True, editable=True)
    time_open = models.DateTimeField(null=True)
    time_start = models.DateTimeField(null=True)
    time_finish = models.DateTimeField(null=True)
    time_close = models.DateTimeField(null=True, verbose_name="Срок выполнения")
    units = models.ManyToManyField(Module, through='Unit')
    dev = models.BooleanField(default=False, null=False, verbose_name="Для тестирования")
    practice = models.BooleanField(default=False)
    duration = models.IntegerField(default=1, verbose_name="Продолжительность темы")
    min_item = models.IntegerField(default=3, verbose_name="Минимальное количество заданий")

    def check_status(self):
        if self.time_close <= timezone.now():
            if self.status == const.TEST_STATUS_OPENED:
                self.status = const.TEST_STATUS_CLOSED
            elif self.status == const.TEST_STATUS_STARTED:
                units = self.units.through.objects.filter(test=self)
                for unit in units:
                    unit.complete()
                    unit.items.through.objects.filter(unit=unit, status=const.ITEM_STATUS_NORESPONSE).delete()
                self.complete()
            self.save()

    def run(self):
        self.time_start = timezone.now()
        self.status = const.TEST_STATUS_STARTED
        self.save()
        self.choose_unit()
        item = self.add_item()
        if item is None:
            self.complete()
        return item

    def complete(self):
        self.time_finish = timezone.now()
        self.status = const.TEST_STATUS_FINISHED
        self.save()

    def check_units_complete(self):
        units = self.units.through.objects.filter(test=self)
        return all([unit.complete_status == const.UNIT_COMPLETE_STATUS_FINISHED
                    for unit in units])

    def get_last_completed_unit(self):
        units = self.units.through.objects.filter(test=self)
        return units.filter(complete_status=const.UNIT_COMPLETE_STATUS_FINISHED).last()

    def get_active_unit(self):
        units = self.units.through.objects.filter(test=self)
        if units.filter(complete_status=const.UNIT_COMPLETE_STATUS_ACTIVE).exists():
            return units.filter(complete_status=const.UNIT_COMPLETE_STATUS_ACTIVE).first()
        else:
            None

    def add_item(self):
        unit = self.get_active_unit()
        if unit is None:
            return None
        task = Task.objects.get_task(unit)
        if task is None:
            unit.complete()
            self.choose_unit()
            return self.add_item()
        else:
            return unit.add_item(task)

    def choose_unit(self):
        units = self.units.through.objects.filter(test=self)
        active_unit = self.get_active_unit()
        if active_unit is not None:
            is_timeout = active_unit.time_left() < 0
            is_enough = active_unit.items.through.objects.filter(unit=active_unit). \
                            exclude(status=const.ITEM_STATUS_NORESPONSE).count() >= active_unit.min_item
            print("timeout", is_timeout)
            print("enough", is_enough)
            if is_enough and is_timeout:
                active_unit.complete()
                active_unit = self.choose_unit()
        elif units.filter(complete_status=const.UNIT_COMPLETE_STATUS_NOTSTARTED).exists():
            active_unit = units.filter(complete_status=const.UNIT_COMPLETE_STATUS_NOTSTARTED).first()
            active_unit.run()
        else:
            return None
        return active_unit


class Unit(models.Model):
    class Meta:
        ordering = ['test__TID', 'order']

    UID = models.IntegerField(unique=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="test_units")
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    items = models.ManyToManyField('domain.Task', through='Item')
    status = models.CharField(max_length=1,
                              choices=const.UNIT_STATUSES_DISPLAY,
                              default=const.UNIT_STATUS_REPEATING)
    order = models.IntegerField()
    complete_status = models.CharField(max_length=1,
                                       choices=const.UNIT_COMPLETE_STATUSES_DISPLAY,
                                       default=const.UNIT_COMPLETE_STATUS_NOTSTARTED)
    duration = models.IntegerField(default=1)
    time_start = models.DateTimeField(null=True)
    time_finish = models.DateTimeField(null=True)
    min_item = models.IntegerField(default=3)

    def run(self):
        self.time_start = timezone.now()
        self.complete_status = const.UNIT_COMPLETE_STATUS_ACTIVE
        self.save()

    def complete(self):
        self.time_finish = timezone.now()
        self.complete_status = const.UNIT_COMPLETE_STATUS_FINISHED
        self.save()

    def time_left(self):
        items = self.items.through.objects.filter(unit=self, time_finish__isnull=False)
        items_duration = timedelta(0)
        for item in items:
            items_duration = items_duration + (item.time_finish - item.time_start)
        if self.get_active_item() is not None:
            items_duration += timezone.now() - self.get_active_item().time_start
        return self.duration * 60 - items_duration.total_seconds()

    def add_item(self, task):
        return Item.objects.create(IID=Item.objects.aggregate(max_IID=Max('IID'))['max_IID'] + 1,
                                   unit=self,
                                   task=task)

    def get_active_item(self):
        items = self.items.through.objects.filter(unit=self)
        if items.filter(status=const.ITEM_STATUS_NORESPONSE).exists():
            return items.filter(status=const.ITEM_STATUS_NORESPONSE).first()
        else:
            return None

    def get_features(self):
        unit_features = {'unit_' + f: self.unitfeature.__dict__['unit_' + f]
                         for f in const.FEATURES}
        module_features = {'module_' + f: self.module.modulefeature.__dict__['module_' + f]
                           for f in const.FEATURES}
        test_features = {'test_' + f: self.test.testfeature.__dict__['test_' + f]
                         for f in const.FEATURES}
        student_features = {'student_' + f: self.module.student.studentfeature.__dict__['student_' + f]
                            for f in const.FEATURES}
        topic_features = {'topic_' + f: self.module.topic.topicfeature.__dict__['topic_' + f]
                          for f in const.FEATURES_DOMAIN}
        return {**topic_features,
                **student_features,
                **module_features,
                **test_features,
                **unit_features}


class Item(models.Model):
    class Meta:
        ordering = ['IID']

    IID = models.IntegerField(unique=True)
    unit = models.ForeignKey(Unit,
                             on_delete=models.CASCADE,
                             related_name='unit_items')
    task = models.ForeignKey('domain.Task',
                             on_delete=models.CASCADE,
                             related_name='task_items')
    response = models.CharField(null=True, max_length=256, verbose_name="Введите ответ")
    valid = models.BooleanField(default=None, null=True)
    status = models.CharField(max_length=1,
                              choices=const.ITEM_STATUSES_DISPLAY,
                              default=const.ITEM_STATUS_NORESPONSE)
    analysis = models.CharField(max_length=1,
                                choices=const.ITEM_ANALYSISES_DISPLAY,
                                default=const.ITEM_ANALYSIS_NONE)
    time_start = models.DateTimeField(null=True)
    time_finish = models.DateTimeField(null=True)
    comment = models.TextField(null=True, blank=True)
    attempts = models.IntegerField(default=0)

    def run(self):
        self.time_start = timezone.now()
        self.save()

    def complete(self):
        self.time_finish = timezone.now()
        self.valid, _ = self.task.check_valid(self.response)
        self.save()
        if self.valid is not None:
            self.task.taskfeature.refresh_features()
            self.unit.unitparam.refresh_params()
            self.unit.module.moduleparam.refresh_params()
            self.unit.module.student.studentparam.refresh_params()

    def complete_incorrect(self):
        self.time_finish = timezone.now()
        self.valid = None
        self.status = const.ITEM_STATUS_INCORRECT
        self.save()

    def complete_difficult(self):
        self.time_finish = timezone.now()
        self.valid = False
        self.status = const.ITEM_STATUS_DIFFICULT
        self.analysis = const.ITEM_ANALYSIS_TODO
        self.save()
