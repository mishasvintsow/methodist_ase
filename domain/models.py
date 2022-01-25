import re

import joblib
import numpy as np
import pandas as pd
from django.db import models
from django.db.models import Manager, Count, Q
from sklearn.preprocessing import PolynomialFeatures

import answers
import const


class Course(models.Model):
    class Meta:
        ordering = ['code']

    code = models.IntegerField(unique=True, verbose_name="Код курса")
    name = models.CharField(max_length=128, unique=True, verbose_name="Название курса")

    def __str__(self):
        return "[%d] %s" % (self.code, self.name)


class Topic(models.Model):
    class Meta:
        ordering = ['code']

    code = models.IntegerField(unique=True, verbose_name="Код темы")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    name = models.CharField(max_length=256, verbose_name="Название темы")
    grade = models.IntegerField(choices=const.GRADES_DISPLAY, default=const.GRADES[0], verbose_name="Класс")

    def __str__(self):
        return "[%d] %s" % (self.code, self.name)


def taskimgpath(instance, filename):
    return 'domain/{0}/{1}.jpg'.format(instance.topic.code, instance.code)


class TaskManager(Manager):
    def get_task(self, unit):
        X_data = pd.DataFrame([{'item__valid': 1, **unit.get_features()}])
        poly = PolynomialFeatures(2)
        X_data = pd.DataFrame(poly.fit_transform(X_data), columns=poly.get_feature_names())
        X_data = X_data[const.MULTIFEATURES]
        rf = joblib.load('randomforest.joblib')
        pred = rf.predict(X_data)[0]

        topic = unit.module.topic
        tasks_in = unit.items
        tasks_qs = self.filter(topic=topic, learning=(unit.status == const.UNIT_STATUS_LEARNING)).exclude(
            code__in=tasks_in.values_list('code', flat=True))
        if tasks_qs.count() == 0:
            return None
        tasks_qs = tasks_qs.annotate(
            item_count=Count('task_items', filter=Q(task_items__unit__test__student=unit.test.student)))
        tasks = pd.DataFrame(tasks_qs.values('code', 'group', 'item_count', 'taskfeature__task_L'))
        if unit.status == const.UNIT_STATUS_LEARNING:
            student_T = unit.module.student.studentfeature.student_T
            from study.models import Item
            items_qs = Item.objects.filter(unit__module=unit.module,
                                           task__code__in=tasks_in.values_list('code', flat=True))
            items = pd.DataFrame(items_qs.values('task__code',
                                                 'task__group',
                                                 'task__taskfeature__task_L',
                                                 'valid'),
                                 columns=['task__code',
                                          'task__group',
                                          'task__taskfeature__task_L',
                                          'valid'])
            groups = {g: len(tasks[tasks['group'] == g].index) for g in tasks['group'].unique().tolist()}

            current_group = []
            for g in sorted(groups.keys()):
                if len(items[items['task__group'] == g].index) <= int(groups[g] * 1 / 3):
                    current_group.append(g)
                    break
                elif int(groups[g] * 1 / 3) < len(items.loc[items['task__group'] == g].index) <= int(groups[g] * 2 / 3):
                    count = int(groups[g] * 2 / 3)
                    last_n = items[items['task__group'] == g].tail(count)
                    success = (last_n[last_n['valid'] == True]['task__taskfeature__task_L'].sum() /
                               (last_n['task__taskfeature__task_L'].sum() + count - len(last_n)))
                    if round(success, 2) <= student_T:
                        current_group.append(g)
                        break
            if current_group == []:
                for g in sorted(groups.keys()):
                    count = int(groups[g] * 2 / 3)
                    last_n = items[items['task__group'] == g].tail(count)
                    success = (last_n[last_n['valid'] == True]['task__taskfeature__task_L'].sum() /
                               (last_n['task__taskfeature__task_L'].sum() + count - len(last_n)))
                    if round(success, 2) <= student_T:
                        current_group.append(g)
                        break
            if current_group == []:
                current_group = tasks['group'].unique().tolist()
            tasks_qs = tasks_qs.filter(group__in=current_group)
            tasks = pd.DataFrame(tasks_qs.values('code', 'group', 'item_count', 'taskfeature__task_L'))

        tasks['level_diff'] = np.abs(tasks['taskfeature__task_L'] - pred)
        group_counts = {group: tasks[tasks['group'] == group]['item_count'].sum() for group in tasks['group'].unique()}
        tasks['group_count'] = list(map(lambda x: group_counts[x], tasks['group']))
        tasks['mul'] = ((1 + tasks['item_count']) / (1 + tasks['item_count'].max())) ** 5 * (
                (1 + tasks['group_count']) / (1 + tasks['group_count'].max())) * tasks['level_diff']
        pred_task = tasks.sort_values('mul').iloc[0]
        return self.get(code=pred_task['code'])


class Task(models.Model):
    class Meta:
        ordering = ['code']

    code = models.IntegerField(unique=True, verbose_name="Код задания")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name="Тема")
    group = models.IntegerField(default=-1, null=True, verbose_name="Группа")
    description = models.TextField(blank=True, verbose_name="Описание")
    draft_answer = models.TextField(default='')
    expert_level = models.IntegerField(choices=const.EXPERT_LEVELS_DISPLAY, default=const.EXPERT_LEVEL_LOW,
                                       verbose_name="Экспертная оценка сложности")
    image = models.ImageField(blank=True, upload_to=taskimgpath, verbose_name="Изображение")
    learning = models.BooleanField(default=False, verbose_name="Для изучения?")
    moderation_status = models.CharField(max_length=1,
                                         choices=const.TASK_MODERATION_STATUSES_DISPLAY,
                                         default=const.TASK_MODERATION_STATUS_UNCHECKED)
    objects = TaskManager()

    def get_answer(self):
        return ";".join(self.answer_set.values_list('text', flat=True))

    def check_valid(self, response):
        if re.search(r';', response) is None:
            responses = [response]
        elif len(const.is_interval(response)) != 0:
            responses = const.is_interval(response)
        else:
            responses = response.split(";")

        answers = self.answer_set
        if len(responses) != answers.count() or responses[0] == ";" or responses[-1] == ";":
            return None, [const.ANSWER_ERROR_WRONG_COUNT]

        responses = list(set(responses))
        columns = range(len(responses))
        indexes = answers.values_list('pk', flat=True)
        valid_matrix = pd.DataFrame([], columns=columns, index=indexes)
        for i in indexes:
            for c in columns:
                valid_matrix.loc[i, c] = answers.get(pk=i).syntax_check(responses[c])
                if valid_matrix.loc[i, c] == const.ANSWER_ERROR_NOT:
                    valid_matrix.loc[i, c] = answers.get(pk=i).semantic_check(responses[c])
        valid_lists = valid_matrix.values.tolist()
        hasnt_errors = all([any([valid in [const.ANSWER_ERROR_RIGHT, const.ANSWER_ERROR_NOT]
                                 for valid in valid_list]) for valid_list in valid_lists])
        if hasnt_errors:
            return all([any([valid == const.ANSWER_ERROR_RIGHT for valid in valid_list])
                        for valid_list in valid_lists]), []

        errors = []
        for valid_list in valid_lists:
            if not any([valid in [const.ANSWER_ERROR_RIGHT, const.ANSWER_ERROR_NOT] for valid in valid_list]):
                errors.extend([valid for valid in valid_list
                               if valid not in [const.ANSWER_ERROR_RIGHT, const.ANSWER_ERROR_NOT]])
        return None, list(set(errors))

    def get_features(self):
        return {'task_' + f: self.taskfeature.__dict__['task_' + f]
                for f in const.FEATURES_DOMAIN}


class Answer(models.Model):
    class Meta:
        ordering = ['code']

    code = models.IntegerField(unique=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    answer_type = models.CharField(max_length=1,
                                   choices=const.ANSWER_TYPES_DISPLAY[1:],
                                   default=const.ANSWER_TYPE_FREE)
    text = models.TextField(default='')

    def set_answer_object(self):
        self.AnswerClass = answers.ANSWER_CLASSES[self.answer_type]
        self.answer_object = self.AnswerClass(text=self.text)
        return self.answer_object

    def syntax_check(self, response):
        try:
            obj = self.answer_object
        except AttributeError:
            obj = self.set_answer_object()
        return obj.syntax_check(response)

    def semantic_check(self, response):
        try:
            obj = self.answer_object
        except AttributeError:
            obj = self.set_answer_object()
        return obj.semantic_check(response)
