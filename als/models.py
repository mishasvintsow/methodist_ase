import math
import os

import numpy as np
import pandas as pd
from django.db import models
from django.utils import timezone
from matplotlib import pyplot as plt

import const
from buduumnee.settings import BASE_DIR
from domain.models import Topic, Task
from lk.models import Student
from study.models import Module, Test, Unit, Item


class TaskFeature(models.Model):
    class Meta:
        ordering = ['task__code']

    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    task_A = models.IntegerField(default=0)
    task_T = models.IntegerField(default=0)
    task_L = models.FloatField(default=0)

    def refresh_features(self):
        items = Item.objects.filter(task=self.task)
        A = 0
        T = 0
        L = const.TASK_LEVEL_INITIAL[self.task.expert_level]
        itemfeatures = []
        for item in items:
            itemf = item.itemfeature
            itemf.task_A = A
            itemf.task_T = T
            itemf.task_L = L
            if item.valid is not None:
                A += 1
                T += int(item.valid)
                L = (L + (A - T) / A) / 2
            itemfeatures.append(itemf)
        ItemFeature.objects.bulk_update(itemfeatures, fields=['task_' + f for f in const.FEATURES_DOMAIN])
        self.task_A = A
        self.task_T = T
        self.task_L = L
        self.save()
        for code in items.order_by('unit__module__topic__code').values_list('unit__module__topic__code',
                                                                            flat=True).distinct():
            Topic.objects.get(code=code).topicfeature.refresh_features()
        for SID in items.order_by('unit__module__student__SID').values_list('unit__module__student__SID',
                                                                            flat=True).distinct():
            Student.objects.get(SID=SID).studentfeature.refresh_features()
        for MID in items.order_by('unit__module__MID').values_list('unit__module__MID', flat=True).distinct():
            Module.objects.get(MID=MID).modulefeature.refresh_features()
        for TID in items.order_by('unit__test__TID').values_list('unit__test__TID', flat=True).distinct():
            Test.objects.get(TID=TID).testfeature.refresh_features()
        for UID in items.order_by('unit__UID').values_list('unit__UID', flat=True).distinct():
            Unit.objects.get(UID=UID).unitfeature.refresh_features()


class TopicFeature(models.Model):
    class Meta:
        ordering = ['topic__code']

    topic = models.OneToOneField(Topic, on_delete=models.CASCADE)
    topic_A = models.IntegerField(default=0)
    topic_T = models.IntegerField(default=0)
    topic_L = models.FloatField(default=0)

    def refresh_features(self):
        items = Item.objects.filter(task__topic=self.topic)
        itemfeatures = []
        A = 0
        T = 0
        L = items.filter(valid=False).count() / items.count() if items.count() else 0.3
        for item in items:
            itemf = item.itemfeature
            itemf.topic_A = A
            itemf.topic_T = T
            itemf.topic_L = L
            if item.valid is not None:
                A += 1
                T += int(item.valid)
                L = (L + (A - T) / A) / 2
            itemfeatures.append(itemf)
        ItemFeature.objects.bulk_update(itemfeatures, fields=['topic_' + f for f in const.FEATURES_DOMAIN])
        self.topic_A = A
        self.topic_T = T
        self.topic_L = L
        self.save()


class StudentFeature(models.Model):
    class Meta:
        ordering = ['student__SID']

    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    student_A = models.IntegerField(default=0)
    student_AL = models.FloatField(default=0)
    student_T = models.IntegerField(default=0)
    student_TL = models.FloatField(default=0)
    student_P = models.FloatField(default=0)
    student_D = models.FloatField(default=0)
    student_R = models.FloatField(default=0)
    student_E = models.FloatField(default=0)

    def refresh_features(self):
        items = Item.objects.filter(unit__module__student=self.student)
        itemfeatures = []
        A = 0
        AL = 0
        T = 0
        TL = 0
        P = 0
        D = 0
        R = 0
        E = 0
        for item in items:
            itemf = item.itemfeature
            itemf.student_A = A
            itemf.student_AL = AL
            itemf.student_T = T
            itemf.student_TL = TL
            itemf.student_P = P
            itemf.student_D = D
            itemf.student_R = R
            itemf.student_E = E
            if item.valid is not None:
                A += 1
                AL += item.task.taskfeature.task_L
                T += int(item.valid)
                TL += int(item.valid) * item.task.taskfeature.task_L
                temp, P = P, TL / AL
                D = P - temp
                temp, R = R, (D / P if P else 0)
                E = (R - temp) / D if D else 0
            itemfeatures.append(itemf)
        ItemFeature.objects.bulk_update(itemfeatures, fields=['student_' + f for f in const.FEATURES])
        self.student_A = A
        self.student_AL = AL
        self.student_T = T
        self.student_TL = TL
        self.student_P = P
        self.student_D = D
        self.student_R = R
        self.student_E = E
        self.save()


class ModuleFeature(models.Model):
    class Meta:
        ordering = ['module__MID']

    module = models.OneToOneField(Module, on_delete=models.CASCADE)
    module_A = models.IntegerField(default=0)
    module_AL = models.FloatField(default=0)
    module_T = models.IntegerField(default=0)
    module_TL = models.FloatField(default=0)
    module_P = models.FloatField(default=0)
    module_D = models.FloatField(default=0)
    module_R = models.FloatField(default=0)
    module_E = models.FloatField(default=0)

    def refresh_features(self):
        items = Item.objects.filter(unit__module=self.module)
        itemfeatures = []
        A = 0
        AL = 0
        T = 0
        TL = 0
        P = 0
        D = 0
        R = 0
        E = 0
        for item in items:
            itemf = item.itemfeature
            itemf.module_A = A
            itemf.module_AL = AL
            itemf.module_T = T
            itemf.module_TL = TL
            itemf.module_P = P
            itemf.module_D = D
            itemf.module_R = R
            itemf.module_E = E
            if item.valid is not None:
                A += 1
                AL += item.task.taskfeature.task_L
                T += int(item.valid)
                TL += int(item.valid) * item.task.taskfeature.task_L
                temp, P = P, TL / AL
                D = P - temp
                temp, R = R, (D / P if P else 0)
                E = (R - temp) / D if D else 0
            itemfeatures.append(itemf)
        ItemFeature.objects.bulk_update(itemfeatures, fields=['module_' + f for f in const.FEATURES])
        self.module_A = A
        self.module_AL = AL
        self.module_T = T
        self.module_TL = TL
        self.module_P = P
        self.module_D = D
        self.module_R = R
        self.module_E = E
        self.save()


class TestFeature(models.Model):
    class Meta:
        ordering = ['test__TID']

    test = models.OneToOneField(Test, on_delete=models.CASCADE)
    test_A = models.IntegerField(default=0)
    test_AL = models.FloatField(default=0)
    test_T = models.IntegerField(default=0)
    test_TL = models.FloatField(default=0)
    test_P = models.FloatField(default=0)
    test_D = models.FloatField(default=0)
    test_R = models.FloatField(default=0)
    test_E = models.FloatField(default=0)

    def refresh_features(self):
        items = Item.objects.filter(unit__module__test=self.test)
        itemfeatures = []
        A = 0
        AL = 0
        T = 0
        TL = 0
        P = 0
        D = 0
        R = 0
        E = 0
        for item in items:
            itemf = item.itemfeature
            itemf.test_A = A
            itemf.test_AL = AL
            itemf.test_T = T
            itemf.test_TL = TL
            itemf.test_P = P
            itemf.test_D = D
            itemf.test_R = R
            itemf.test_E = E
            if item.valid is not None:
                A += 1
                AL += item.task.taskfeature.task_L
                T += int(item.valid)
                TL += int(item.valid) * item.task.taskfeature.task_L
                temp, P = P, TL / AL
                D = P - temp
                temp, R = R, (D / P if P else 0)
                E = (R - temp) / D if D else 0
            itemfeatures.append(itemf)
        ItemFeature.objects.bulk_update(itemfeatures, fields=['test_' + f for f in const.FEATURES])
        self.test_A = A
        self.test_AL = AL
        self.test_T = T
        self.test_TL = TL
        self.test_P = P
        self.test_D = D
        self.test_R = R
        self.test_E = E
        self.save()


class UnitFeature(models.Model):
    class Meta:
        ordering = ['unit__UID']

    unit = models.OneToOneField(Unit, on_delete=models.CASCADE)
    unit_A = models.IntegerField(default=0)
    unit_AL = models.FloatField(default=0)
    unit_T = models.IntegerField(default=0)
    unit_TL = models.FloatField(default=0)
    unit_P = models.FloatField(default=0)
    unit_D = models.FloatField(default=0)
    unit_R = models.FloatField(default=0)
    unit_E = models.FloatField(default=0)

    def refresh_features(self):
        items = Item.objects.filter(unit=self.unit)
        itemfeatures = []
        A = 0
        AL = 0
        T = 0
        TL = 0
        P = 0
        D = 0
        R = 0
        E = 0
        for item in items:
            itemf = item.itemfeature
            itemf.unit_A = A
            itemf.unit_AL = AL
            itemf.unit_T = T
            itemf.unit_TL = TL
            itemf.unit_P = P
            itemf.unit_D = D
            itemf.unit_R = R
            itemf.unit_E = E
            if item.valid is not None:
                A += 1
                AL += item.task.taskfeature.task_L
                T += int(item.valid)
                TL += int(item.valid) * item.task.taskfeature.task_L
                temp, P = P, TL / AL
                D = P - temp
                temp, R = R, (D / P if P else 0)
                E = (R - temp) / D if D else 0
            itemfeatures.append(itemf)
        ItemFeature.objects.bulk_update(itemfeatures, fields=['unit_' + f for f in const.FEATURES])
        self.unit_A = A
        self.unit_AL = AL
        self.unit_T = T
        self.unit_TL = TL
        self.unit_P = P
        self.unit_D = D
        self.unit_R = R
        self.unit_E = E
        self.save()


class ItemFeature(models.Model):
    class Meta:
        ordering = ['item__IID']

    item = models.OneToOneField(Item, on_delete=models.CASCADE)

    task_A = models.IntegerField(default=0)
    task_T = models.IntegerField(default=0)
    task_L = models.FloatField(default=0)

    topic_A = models.IntegerField(default=0)
    topic_T = models.IntegerField(default=0)
    topic_L = models.FloatField(default=0)

    student_A = models.IntegerField(default=0)
    student_AL = models.FloatField(default=0)
    student_T = models.IntegerField(default=0)
    student_TL = models.FloatField(default=0)
    student_P = models.FloatField(default=0)
    student_D = models.FloatField(default=0)
    student_R = models.FloatField(default=0)
    student_E = models.FloatField(default=0)

    module_A = models.IntegerField(default=0)
    module_AL = models.FloatField(default=0)
    module_T = models.IntegerField(default=0)
    module_TL = models.FloatField(default=0)
    module_P = models.FloatField(default=0)
    module_D = models.FloatField(default=0)
    module_R = models.FloatField(default=0)
    module_E = models.FloatField(default=0)

    test_A = models.IntegerField(default=0)
    test_AL = models.FloatField(default=0)
    test_T = models.IntegerField(default=0)
    test_TL = models.FloatField(default=0)
    test_P = models.FloatField(default=0)
    test_D = models.FloatField(default=0)
    test_R = models.FloatField(default=0)
    test_E = models.FloatField(default=0)

    unit_A = models.IntegerField(default=0)
    unit_AL = models.FloatField(default=0)
    unit_T = models.IntegerField(default=0)
    unit_TL = models.FloatField(default=0)
    unit_P = models.FloatField(default=0)
    unit_D = models.FloatField(default=0)
    unit_R = models.FloatField(default=0)
    unit_E = models.FloatField(default=0)


class StudentParam(models.Model):
    class Meta:
        ordering = ['student__SID']

    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    PRT = models.FloatField(null=True)  # процент правильно решенных заданий по всем темам
    MCET = models.FloatField(null=True)  # средняя сложность всех разобранных заданий
    MRPRT = models.FloatField(null=True)  # средний процент правильных по темам в статусе повторение

    def refresh_params(self):
        items = Item.objects.filter(unit__test__student=self.student).filter(valid__isnull=False)
        self.PRT = round(100 * items.filter(valid=True).count() / items.count(), 2) if items.count() else None
        self.MCET = round(np.mean(items.values_list('task__taskfeature__task_L', flat=True)),
                          3) if items.count() else None
        if self.student.modules.filter(moduleparam__RPRT__isnull=False).exists():
            self.MRPRT = np.mean(self.student.modules.filter(moduleparam__RPRT__isnull=False).values_list('moduleparam__RPRT', flat=True))
        else:
            self.MRPRT = 0
        self.save()

    @property
    def k(self):
        return Item.objects.filter(unit__module__student=self.student,
                                   status__in=[const.ITEM_STATUS_UNCLEAR, const.ITEM_STATUS_DIFFICULT],
                                   analysis=const.ITEM_ANALYSIS_TODO).count()

    @property
    def m(self):
        return Item.objects.filter(unit__module__student=self.student,
                                   status=const.ITEM_STATUS_CLEAR,
                                   analysis=const.ITEM_ANALYSIS_TODO).count()

    @property
    def tests_finished_count(self):
        return self.student.tests.filter(practice=False, status=const.TEST_STATUS_FINISHED).count()

    @property
    def tests_unfinished_count(self):
        signs = 0
        for test in self.student.tests.filter(practice=False).order_by("-time_create"):
            if test.status != const.TEST_STATUS_FINISHED:
                signs += 1
            elif test.status == const.TEST_STATUS_FINISHED or signs >= 3:
                break
        return range(signs)

    @property
    def practices_finished_count(self):
        return self.student.tests.filter(practice=True, status=const.TEST_STATUS_FINISHED).count()


class ModuleParam(models.Model):
    class Meta:
        ordering = ['module__student__SID', 'module__order']

    module = models.OneToOneField(Module, on_delete=models.CASCADE)
    LPEG = models.FloatField(
        null=True)  # процент разобранных групп при изучении (learning percentage of explored groups)
    LPET = models.FloatField(
        null=True)  # процент разобранных заданий при изучении (learning percentage of explored tasks)
    LPRT = models.FloatField(
        null=True)  # процент правильно выполненных заданий при изучении (learning percentage of right tasks)
    LGPT = models.JSONField(null=True)  # процент разобранных заданий по группам при изучении
    RPRT = models.FloatField(
        null=True)  # процент правильно выполненных заданий при повторении (repeating percentage of right tasks)
    RMCAT = models.FloatField(null=True)  # средняя сложность среди всех задач
    RMCRT = models.FloatField(null=True)  # средняя сложность среди правильных задач
    RMCR5T = models.FloatField(null=True)  # средняя сложность среди 5 самых сложных правильных заданий
    RRCRtoCA = models.FloatField(null=True)  # отношение сложности правильных к сложности всех
    RMCAtoPR = models.FloatField(null=True)  # произведение средней сложности всех на процент правильных
    color = models.CharField(max_length=1, choices=const.MODULE_COLORS_DISPLAY, default=const.MODULE_COLOR_EMPTY)

    def refresh_params(self):
        items = Item.objects.filter(unit__module=self.module).filter(valid__isnull=False)
        tasks = Task.objects.filter(topic=self.module.topic)
        items_l = items.filter(task__learning=True)
        tasks_l = tasks.filter(learning=True)
        groups_l = tasks_l.order_by('group').values_list('group', flat=True).distinct()
        groups_by_items = items_l.order_by('task__group').values_list('task__group').distinct()
        tasks_by_items = items.order_by('task__code').values_list('task__code').distinct()
        self.LPEG = round(100 * groups_by_items.count() / groups_l.count(),
                          1) if groups_l.count() and items_l.exists() else None
        self.LPET = round(100 * tasks_by_items.count() / tasks_l.count(),
                          1) if tasks_l.count() and items_l.exists() else None
        self.LPRT = round(100 * items_l.filter(valid=True).count() / items_l.count(), 2) if items_l.count() else None
        self.LGPT = {group: {'all': tasks_l.filter(group=group).count(),
                             'items': tasks_by_items.filter(task__group=group).count(),
                             'explored_rate': (round(
                                 100 * tasks_by_items.filter(task__group=group).count() / tasks_l.filter(
                                     group=group).count(), 1)
                                               if tasks_l.filter(group=group).count() else None),
                             'attempts': items_l.filter(task__group=group).count(),
                             'right': items_l.filter(task__group=group, valid=True).count(),
                             'right_rate': (round(
                                 100 * items_l.filter(task__group=group, valid=True).count() / items_l.filter(
                                     task__group=group).count(), 1)
                                            if items_l.filter(task__group=group).count() else None)} for group in
                     groups_l}
        items_r = items.filter(task__learning=False)
        levels_all = items_r.values_list('task__taskfeature__task_L', flat=True)
        levels_true = items_r.filter(valid=True).values_list('task__taskfeature__task_L', flat=True)
        self.RPRT = round(100 * items_r.filter(valid=True).count() / items_r.count(), 1) if items_r.count() else None
        self.RMCAT = round(np.mean(levels_all), 3) if levels_all else None
        self.RMCRT = (round(np.mean(levels_true), 3) if levels_true else 0) if levels_all else None
        self.RMCR5T = round(np.mean(levels_true.order_by('-task__taskfeature__task_L')[:5]), 3) if levels_true else None
        self.RRCRtoCA = round(100 * (np.sum(levels_true) if levels_true else 0) / np.sum(levels_all),
                              1) if levels_all else None
        self.RMCAtoPR = round(self.RMCAT * self.RPRT, 1) if self.RMCAT is not None and self.RPRT is not None else None
        if self.module.unit_set.filter(unitparam__RPRT__isnull=False).count() >= 2:
            unitp_last = self.module.unit_set.filter(unitparam__RPRT__isnull=False).order_by('-time_start')[0].unitparam
            unitp_prev = self.module.unit_set.filter(unitparam__RPRT__isnull=False).order_by('-time_start')[1].unitparam
            if unitp_last.RPRT < unitp_prev.RPRT:
                if unitp_last.RPRT < self.RPRT:
                    self.color = const.MODULE_COLOR_RED
                else:
                    self.color = const.MODULE_COLOR_PINK
            else:
                if unitp_last.RPRT > self.RPRT:
                    self.color = const.MODULE_COLOR_GREEN
                else:
                    self.color = const.MODULE_COLOR_EMPTY
        else:
            self.color = const.MODULE_COLOR_EMPTY
        self.save()

    @property
    def RMCAT_10(self):
        return math.ceil(10 * self.RMCAT)

    @property
    def last_unit_RPRT(self):
        if self.module.unit_set.filter(time_finish__isnull=False).exists():
            unit = self.module.unit_set.filter(time_finish__isnull=False).order_by('-time_finish').first()
            return unit.unitparam.RPRT
        else:
            return None

    @property
    def prevlast_unit_RPRT(self):
        if self.module.unit_set.filter(time_finish__isnull=False).count() > 1:
            unit = self.module.unit_set.filter(time_finish__isnull=False).order_by('-time_finish')[1]
            return unit.unitparam.RPRT
        else:
            return None

    @property
    def last_unit_RPRT(self):
        if self.module.unit_set.filter(time_finish__isnull=False).exists():
            unit = self.module.unit_set.filter(time_finish__isnull=False).order_by('-time_finish').first()
            return unit.unitparam.RPRT
        else:
            return None

    @property
    def prevlast_unit_RMCAT(self):
        if self.module.unit_set.filter(time_finish__isnull=False).count() > 1:
            unit = self.module.unit_set.filter(time_finish__isnull=False).order_by('-time_finish')[1]
            return unit.unitparam.RMCAT
        else:
            return None

    @property
    def last_unit_RMCAT(self):
        if self.module.unit_set.filter(time_finish__isnull=False).exists():
            unit = self.module.unit_set.filter(time_finish__isnull=False).order_by('-time_finish').first()
            return unit.unitparam.RMCAT
        else:
            return None

    @property
    def prevlast_unit_RMCRT(self):
        if self.module.unit_set.filter(time_finish__isnull=False).count() > 1:
            unit = self.module.unit_set.filter(time_finish__isnull=False).order_by('-time_finish')[1]
            return unit.unitparam.RMCRT
        else:
            return None

    @property
    def last_unit_RMCRT(self):
        if self.module.unit_set.filter(time_finish__isnull=False).exists():
            unit = self.module.unit_set.filter(time_finish__isnull=False).order_by('-time_finish').first()
            return unit.unitparam.RMCRT
        else:
            return None

    @property
    def prevlast_unit_RRCRtoCA(self):
        if self.module.unit_set.filter(time_finish__isnull=False).count() > 1:
            unit = self.module.unit_set.filter(time_finish__isnull=False).order_by('-time_finish')[1]
            return unit.unitparam.RRCRtoCA
        else:
            return None

    @property
    def last_unit_RRCRtoCA(self):
        if self.module.unit_set.filter(time_finish__isnull=False).exists():
            unit = self.module.unit_set.filter(time_finish__isnull=False).order_by('-time_finish').first()
            return unit.unitparam.RRCRtoCA
        else:
            return None

    @property
    def prevlast_unit_RMCAtoPR(self):
        if self.module.unit_set.filter(time_finish__isnull=False).count() > 1:
            unit = self.module.unit_set.filter(time_finish__isnull=False).order_by('-time_finish')[1]
            return unit.unitparam.RMCAtoPR
        else:
            return None

    @property
    def last_unit_RMCAtoPR(self):
        if self.module.unit_set.filter(time_finish__isnull=False).exists():
            unit = self.module.unit_set.filter(time_finish__isnull=False).order_by('-time_finish').first()
            return unit.unitparam.RMCAtoPR
        else:
            return None

    @property
    def k(self):
        return Item.objects.filter(unit__module=self.module,
                                   status__in=[const.ITEM_STATUS_UNCLEAR, const.ITEM_STATUS_DIFFICULT],
                                   analysis=const.ITEM_ANALYSIS_TODO).count()

    @property
    def m(self):
        return Item.objects.filter(unit__module=self.module,
                                   status=const.ITEM_STATUS_CLEAR,
                                   analysis=const.ITEM_ANALYSIS_TODO).count()

    def make_plots(self):
        units = Unit.objects.filter(module=self.module, time_start__isnull=False).order_by('time_finish')
        xticks = []
        xdata = []
        ydata_RPRT = []
        ydata_RMCAT = []
        ydata_RMCRT = []
        ydata_RRCRtoCA = []
        ydata_RMCAtoPR = []
        durations = []

        if units.exists():
            dates = list(units.values_list('test__TID', 'time_finish')) + [('Now', timezone.now())]

            for i, date in enumerate(dates):
                if date[1] is None:
                    dates[i] = ('Now', timezone.now())
            for i, date in enumerate(dates[:-1]):
                xdata.append(str(date[0]) + ": " + date[1].strftime("%d/%m"))
                xdata.append(str(date[0]) + ": " + date[1].strftime("%d/%m") + " ")
                xticks.append(str(date[0]) + ": " + date[1].strftime("%d/%m"))
                xticks.append("")

                delta = (dates[i + 1][1] - date[1]).total_seconds() / (60 * 60) or 0
                durations.append("%d д. %d ч." % divmod(delta, 24))

            for unit in units:
                ydata_RPRT.append((unit.unitparam.RPRT if unit.unitparam.RPRT is not None else 0))
                ydata_RPRT.append(0)
                ydata_RMCAT.append(10 * (unit.unitparam.RMCAT if unit.unitparam.RMCAT is not None else 0))
                ydata_RMCAT.append(0)
                ydata_RMCRT.append(10 * (unit.unitparam.RMCRT if unit.unitparam.RMCRT is not None else 0))
                ydata_RMCRT.append(0)
                ydata_RRCRtoCA.append((unit.unitparam.RRCRtoCA if unit.unitparam.RRCRtoCA is not None else 0))
                ydata_RRCRtoCA.append(0)
                ydata_RMCAtoPR.append((unit.unitparam.RMCAtoPR if unit.unitparam.RMCAtoPR is not None else 0))
                ydata_RMCAtoPR.append(0)
        plt.ioff()
        fig = plt.figure()
        print(ydata_RPRT)
        plt.bar(xdata, ydata_RPRT)
        plt.title("Процент правильно выполненных заданий")
        plt.ylabel("RPRT")
        plt.xticks(np.arange(len(xticks) + 1), xticks + [""], rotation=45)
        plt.xlabel("Тесты (ID: дата)")
        plt.yticks(range(0, 110, 10))
        plt.grid(True)
        plt.grid(which='minor', axis='both', zorder=-1.0)

        for i, d in enumerate(durations):
            plt.text(2 * i + 1, 10, d, rotation=90, ha="center")
        plt.savefig(BASE_DIR / 'static' / 'images' / 'plots' / ('module_%d_RPRT.jpg' % (self.module.MID)),
                    bbox_inches='tight')
        plt.close(fig)

        fig = plt.figure()
        plt.bar(xdata, ydata_RMCAT)
        plt.title("Средняя сложность всех разобранных заданий")
        plt.ylabel("RMCAT")
        plt.xticks(np.arange(len(xticks) + 1), xticks + [""], rotation=45)
        plt.xlabel("Тесты (ID: дата)")
        plt.yticks(range(0, 11))
        plt.grid(True)
        plt.grid(which='minor', axis='both', zorder=-1.0)

        for i, d in enumerate(durations):
            plt.text(2 * i + 1, 1, d, rotation=90, ha="center")
        plt.savefig(BASE_DIR / 'static' / 'images' / 'plots' / ('module_%d_RMCAT.jpg' % (self.module.MID)),
                    bbox_inches='tight')
        plt.close(fig)

        fig = plt.figure()
        plt.bar(xdata, ydata_RMCRT)
        plt.title("Средняя сложность правильных заданий")
        plt.ylabel("RMCRT")
        plt.xticks(np.arange(len(xticks) + 1), xticks + [""], rotation=45)
        plt.xlabel("Тесты (ID: дата)")
        plt.yticks(range(0, 11))
        plt.grid(True)
        plt.grid(which='minor', axis='both', zorder=-1.0)

        for i, d in enumerate(durations):
            plt.text(2 * i + 1, 1, d, rotation=90, ha="center")
        plt.savefig(BASE_DIR / 'static' / 'images' / 'plots' / ('module_%d_RMCRT.jpg' % (self.module.MID)),
                    bbox_inches='tight')
        plt.close(fig)

        fig = plt.figure()
        plt.bar(xdata, ydata_RRCRtoCA)
        plt.ylabel("RRCRtoCA")
        plt.title("Отношение суммы сложностей правильных\nк сумме сложностей заданий")
        plt.xticks(np.arange(len(xticks) + 1), xticks + [""], rotation=45)
        plt.xlabel("Тесты (ID: дата)")
        plt.yticks(range(0, 101, 10))
        plt.grid(True)
        plt.grid(which='minor', axis='both', zorder=-1.0)

        for i, d in enumerate(durations):
            plt.text(2 * i + 1, 10, d, rotation=90, ha="center")
        plt.savefig(BASE_DIR / 'static' / 'images' / 'plots' / ('module_%d_RRCRtoCA.jpg' % (self.module.MID)),
                    bbox_inches='tight')
        plt.close(fig)

        fig = plt.figure()
        plt.bar(xdata, ydata_RMCAtoPR)
        plt.ylabel("RMCAtoPR")
        plt.title("Произведение средней сложности всех\nна процент правильных из всех разобранных")
        plt.xticks(np.arange(len(xticks) + 1), xticks + [""], rotation=45)
        plt.xlabel("Тесты (ID: дата)")
        plt.yticks(range(0, 101, 10))
        plt.grid(True)
        plt.grid(which='minor', axis='both', zorder=-1.0)

        for i, d in enumerate(durations):
            plt.text(2 * i + 1, 10, d, rotation=90, ha="center")
        plt.savefig(BASE_DIR / 'static' / 'images' / 'plots' / ('module_%d_RMCAtoPR.jpg' % (self.module.MID)),
                    bbox_inches='tight')
        plt.close(fig)

        fig = plt.figure()
        plt.title("Распределение правильность-сложность")
        plt.xticks(range(0, 11))
        plt.xlabel("Сложность")
        plt.yticks([r / 10 for r in range(0, 11)])
        plt.ylabel("Правильность")
        plt.grid(True)
        plt.grid(which="minor", axis='both', zorder=0)
        if Item.objects.filter(unit__module=self.module, valid__isnull=False).exists():
            items = pd.DataFrame(Item.objects.filter(unit__module=self.module,
                                                     valid__isnull=False).values_list('valid', 'task__taskfeature__task_L'),
                                 columns=['valid', 'level'])
            items['valid'] = items['valid'].apply(lambda x: int(x))
            items['level'] = items['level'].apply(lambda x: math.ceil(10 * x))
            items = items.groupby('level').mean().reindex(range(1, 11)).fillna(0)
            plt.bar(items.index, items['valid'])
        plt.savefig(BASE_DIR / 'static' / 'images' / 'plots' / ('module_%d_DCR.jpg' % (self.module.MID)),
                    bbox_inches='tight')
        plt.close(fig)

    @property
    def get_plot_RPRT(self):
        path = 'images/plots/module_%d_RPRT.jpg' % self.module.MID
        if os.path.exists(BASE_DIR/'static'/path):
            return '/'+path
        else:
            return None

    @property
    def get_plot_RMCAT(self):
        path = 'images/plots/module_%d_RMCAT.jpg' % self.module.MID
        if os.path.exists(BASE_DIR/'static'/path):
            return '/'+path
        else:
            return None

    @property
    def get_plot_RMCRT(self):
        path = 'images/plots/module_%d_RMCRT.jpg' % self.module.MID
        if os.path.exists(BASE_DIR / 'static' / path):
            return '/' + path
        else:
            return None

    @property
    def get_plot_RRCRtoCA(self):
        path = 'images/plots/module_%d_RRCRtoCA.jpg' % self.module.MID
        if os.path.exists(BASE_DIR / 'static' / path):
            return '/' + path
        else:
            return None

    @property
    def get_plot_RMCAtoPR(self):
        path = 'images/plots/module_%d_RMCAtoPR.jpg' % self.module.MID
        if os.path.exists(BASE_DIR / 'static' / path):
            return '/' + path
        else:
            return None

    @property
    def get_plot_DCR(self):
        path = 'images/plots/module_%d_DCR.jpg' % self.module.MID
        if os.path.exists(BASE_DIR / 'static' / path):
            return '/' + path
        else:
            return None


class UnitParam(models.Model):
    class Meta:
        ordering = ['unit__test__TID', 'unit__order']

    unit = models.OneToOneField(Unit, on_delete=models.CASCADE)
    RPRT = models.FloatField(
        null=True)  # процент правильно выполненных заданий при повторении (repeating percentage of right tasks)
    RMCAT = models.FloatField(null=True)  # средняя сложность среди всех задач
    RMCRT = models.FloatField(null=True)  # средняя сложность среди правильных задач
    RRCRtoCA = models.FloatField(null=True)  # отношение сложности правильных к сложности всех
    RMCAtoPR = models.FloatField(null=True)  # произведение средней сложности всех на процент правильных

    def refresh_params(self):
        items = Item.objects.filter(unit=self.unit).filter(valid__isnull=False)
        tasks = Task.objects.filter(topic=self.unit.module.topic)
        items_r = items.filter(task__learning=False)
        levels_all = items_r.values_list('task__taskfeature__task_L', flat=True)
        levels_true = items_r.filter(valid=True).values_list('task__taskfeature__task_L', flat=True)
        self.RPRT = round(100 * items_r.filter(valid=True).count() / items_r.count(), 1) if items_r.count() else None
        self.RMCAT = round(np.mean(levels_all), 3) if levels_all else None
        self.RMCRT = (round(np.mean(levels_true), 3) if levels_true else 0) if levels_all else None
        self.RRCRtoCA = round(100 * (np.sum(levels_true) if levels_true else 0) / np.sum(levels_all),
                              1) if levels_all else None
        self.RMCAtoPR = round(self.RMCAT * self.RPRT, 1) if self.RMCAT is not None and self.RPRT is not None else None
        self.save()
