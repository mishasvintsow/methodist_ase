import os
import zipfile
from shutil import rmtree

import numpy as np
import pandas as pd
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files import File
from django.db.models import Q
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, FormView, DeleteView
from django.views.generic.list import ListView

import const
from buduumnee import settings
from mixins import UserPermissionsMixin
from domain.forms import CourseCreateUpdateForm, TopicCreateUpdateForm, TaskCreateUpdateForm, TaskSolveForm, \
    TaskPlugForm, AnswersFormSet, FileUploadForm, TopicsFormSet
from domain.models import Course, Topic, Task, Answer


class DomainIndexView(LoginRequiredMixin, UserPermissionsMixin, TemplateView):
    access = const.PROFILE_ROLES_TECH
    template_name = "domain/index.html"


class CoursesListView(LoginRequiredMixin, UserPermissionsMixin, ListView):
    access = const.PROFILE_ROLES_TECH
    template_name = "domain/courses_list.html"
    model = Course
    context_object_name = "courses"


class CourseCreateView(LoginRequiredMixin, UserPermissionsMixin, CreateView):
    access = const.PROFILE_ROLES_TECH
    template_name = "domain/course_create.html"
    model = Course
    form_class = CourseCreateUpdateForm

    def get_success_url(self, **kwargs):
        return reverse_lazy("course_detail", args=(self.object.code,))


class CourseUpdateView(LoginRequiredMixin, UserPermissionsMixin, UpdateView):
    access = const.PROFILE_ROLES_TECH
    template_name = "domain/course_update.html"
    model = Course
    form_class = CourseCreateUpdateForm

    def get_object(self, **kwargs):
        return get_object_or_404(Course, code=self.kwargs['code'])

    def get_success_url(self, **kwargs):
        return reverse_lazy("course_detail", args=(self.object.code,))


class CourseDetailView(LoginRequiredMixin, UserPermissionsMixin, DetailView):
    access = const.PROFILE_ROLES_TECH
    template_name = "domain/course_detail.html"
    model = Course
    context_object_name = 'course'

    def get_object(self, **kwargs):
        return get_object_or_404(Course, code=self.kwargs['code'])


class CourseDeleteView(LoginRequiredMixin, UserPermissionsMixin, RedirectView):
    access = const.PROFILE_ROLES_ADMIN
    url = None

    def get_redirect_url(self, code):
        course = get_object_or_404(Course, code=code)
        course.delete()
        self.url = self.request.META.get('HTTP_REFERER', '/')
        return super(CourseDeleteView, self).get_redirect_url()


class TopicsListView(LoginRequiredMixin, UserPermissionsMixin, ListView):
    access = const.PROFILE_ROLES_TECH
    template_name = "domain/topics_list.html"
    model = Topic
    context_object_name = "topics"

    def get_queryset(self):
        topics = Topic.objects.all()
        if 'code' in self.kwargs:
            topics = topics.filter(course__code=self.kwargs['code'])
        return topics

    def get_context_data(self, **kwargs):
        context = super(TopicsListView, self).get_context_data()
        context['course'] = Course.objects.get(code=self.kwargs['code']).name if 'code' in self.kwargs else None
        return context


class TopicCreateView(LoginRequiredMixin, UserPermissionsMixin, CreateView):
    access = const.PROFILE_ROLES_TECH
    template_name = "domain/topic_create.html"
    model = Topic
    form_class = TopicCreateUpdateForm

    def get_success_url(self, **kwargs):
        return reverse_lazy("topic_detail", args=(self.object.code,))


class TopicUpdateView(LoginRequiredMixin, UserPermissionsMixin, UpdateView):
    access = const.PROFILE_ROLES_TECH
    template_name = "domain/topic_update.html"
    model = Topic
    form_class = TopicCreateUpdateForm

    def get_object(self, **kwargs):
        return get_object_or_404(Topic, code=self.kwargs['code'])

    def get_success_url(self, **kwargs):
        return reverse_lazy("topic_detail", args=(self.object.code,))


class TopicDetailView(LoginRequiredMixin, UserPermissionsMixin, DetailView):
    access = const.PROFILE_ROLES_TECH
    template_name = "domain/topic_detail.html"
    model = Topic
    context_object_name = 'topic'

    def get_object(self, **kwargs):
        return get_object_or_404(Topic, code=self.kwargs['code'])


class TopicDeleteView(LoginRequiredMixin, UserPermissionsMixin, RedirectView):
    access = const.PROFILE_ROLES_ADMIN
    url = None

    def get_redirect_url(self, code):
        topic = get_object_or_404(Topic, code=code)
        topic.delete()
        self.url = self.request.META.get('HTTP_REFERER', '/')
        return super(TopicDeleteView, self).get_redirect_url()


class AnswersListView(LoginRequiredMixin, UserPermissionsMixin, ListView):
    access = const.PROFILE_ROLES_TECH
    template_name = "domain/answers_list.html"
    model = Answer
    context_object_name = "answers"
    paginate_by = 50


class TasksListView(LoginRequiredMixin, UserPermissionsMixin, ListView):
    access = const.PROFILE_ROLES_TECH
    template_name = "domain/tasks_list.html"
    model = Task
    context_object_name = "tasks"
    paginate_by = 20

    def get_queryset(self):
        tasks = super(TasksListView, self).get_queryset()
        if 'code' in self.kwargs:
            tasks = tasks.filter(topic__code=self.kwargs['code'])
        return tasks

    def get_context_data(self, **kwargs):
        context = super(TasksListView, self).get_context_data()
        context['topic'] = Topic.objects.get(code=self.kwargs['code']).name if 'code' in self.kwargs else None
        return context


class TaskCreateView(LoginRequiredMixin, UserPermissionsMixin, CreateView):
    access = const.PROFILE_ROLES_TECH
    template_name = "domain/task_create.html"
    model = Task
    form_class = TaskCreateUpdateForm

    def get_success_url(self, **kwargs):
        return reverse_lazy("task_detail", args=(self.object.code,))


class TaskUpdateView(LoginRequiredMixin, UserPermissionsMixin, UpdateView):
    access = const.PROFILE_ROLES_TECH
    template_name = "domain/task_update.html"
    model = Task
    form_class = TaskCreateUpdateForm

    def get_object(self, **kwargs):
        return get_object_or_404(Task, code=self.kwargs['code'])

    def get_success_url(self, **kwargs):
        return reverse_lazy("task_detail", args=(self.object.code,))


class TaskDetailView(LoginRequiredMixin, UserPermissionsMixin, DetailView):
    access = const.PROFILE_ROLES_TECH
    template_name = "domain/task_detail.html"
    model = Task
    context_object_name = 'task'

    def get_object(self, **kwargs):
        return get_object_or_404(Task, code=self.kwargs['code'])


class TaskDeleteView(LoginRequiredMixin, UserPermissionsMixin, RedirectView):
    access = const.PROFILE_ROLES_ADMIN
    url = None

    def get_redirect_url(self, code):
        task = get_object_or_404(Task, code=code)
        task.delete()
        self.url = self.request.META.get('HTTP_REFERER', '/')
        return super(TaskDeleteView, self).get_redirect_url()


class TaskSolveView(SuccessMessageMixin, LoginRequiredMixin, UserPermissionsMixin, UpdateView):
    access = const.PROFILE_ROLES_TECH
    template_name = "domain/task_solve_view.html"
    model = Task
    form_class = TaskSolveForm
    context_object_name = 'task'
    success_message = "Правильно!"

    def get_object(self, **kwargs):
        return get_object_or_404(Task, code=self.kwargs['code'])

    def get_success_url(self, **kwargs):
        return reverse_lazy('task_solve', args=(self.object.code,))


class AnswersUpdateView(LoginRequiredMixin, UserPermissionsMixin, UpdateView):
    access = const.PROFILE_ROLES_TECH
    template_name = "domain/answers_update.html"
    model = Task
    form_class = TaskPlugForm

    def get_object(self, **kwargs):
        return get_object_or_404(Task, code=self.kwargs['code'])

    def get_context_data(self, **kwargs):
        context = super(AnswersUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = AnswersFormSet(self.request.POST, instance=self.object)
            context['formset'].full_clean()
        else:
            context['formset'] = AnswersFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['formset']
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy("answers_update", args=(self.object.code,))


class TopicsFileUploadView(LoginRequiredMixin, UserPermissionsMixin, FormView):
    access = const.PROFILE_ROLES_ADMIN
    template_name = "domain/topics_xls_upload.html"
    form_class = FileUploadForm

    def form_valid(self, form):
        try:
            file_object = self.request.FILES.get("file")
            with open(settings.BASE_DIR / "media" / "domain" / "topics.xls", 'wb+') as destination:
                for chunk in file_object.chunks():
                    destination.write(chunk)
            df = pd.read_excel(settings.BASE_DIR / "media" / "domain" / "topics.xls")
            if df.isnull().values.any():
                return super().form_invalid(form)
        except Exception as e:
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy("topics_upload_check")

    def get_context_data(self, **kwargs):
        context = super(TopicsFileUploadView, self).get_context_data(**kwargs)
        context['min_code'] = min(Topic.objects.all().values_list('code', flat=True))
        context['max_code'] = max(Topic.objects.all().values_list('code', flat=True))
        return context


class TopicsFileCheckView(LoginRequiredMixin, UserPermissionsMixin, UpdateView):
    access = const.PROFILE_ROLES_ADMIN
    template_name = "domain/topics_file_check.html"
    model = Course
    form_class = CourseCreateUpdateForm

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_exist = True
        try:
            initial_data = pd.read_excel(settings.BASE_DIR / "media" / "domain" / "topics.xls",
                                         index_col=False).to_dict('records')
            self.equal_rows = [row for row in initial_data if Topic.objects.filter(code=row['code'],
                                                                                   name=row['name'],
                                                                                   grade=row['grade']).exists()]
            self.new_rows = [row for row in initial_data if not Topic.objects.filter(code=row['code']).exists()]
            self.existing_rows = [row for row in initial_data if Topic.objects.filter(
                Q(code=row['code']) & ~Q(name=row['name']) & ~Q(grade=row['grade'])).exists()]
        except FileNotFoundError:
            self.file_exist = False

    def get_object(self, **kwargs):
        return Course.objects.get(code=1)

    def get_context_data(self, **kwargs):
        context = super(TopicsFileCheckView, self).get_context_data(**kwargs)
        context['file_exist'] = self.file_exist
        if self.file_exist:
            existing_instances = Topic.objects.filter(code__in=[row['code'] for row in self.existing_rows])
            context['existing_instances'] = existing_instances
            equal_instances = Topic.objects.filter(code__in=[row['code'] for row in self.equal_rows])
            context['equal_instances'] = equal_instances

            if self.request.POST:
                context['new_formset'] = TopicsFormSet(self.request.POST,
                                                       instance=self.object,
                                                       prefix="new")
                context['existing_formset'] = TopicsFormSet(self.request.POST,
                                                            instance=self.object,
                                                            prefix="existing")
                context['new_formset'].full_clean()
                context['existing_formset'].full_clean()
            else:
                context['new_formset'] = TopicsFormSet(queryset=Topic.objects.none(),
                                                       instance=self.object,
                                                       prefix="new")
                context['new_formset'].initial = self.new_rows
                context['new_formset'].extra = len(self.new_rows)
                context['existing_formset'] = TopicsFormSet(queryset=existing_instances,
                                                            instance=self.object,
                                                            prefix="existing")
                context['existing_formset'].initial = self.existing_rows
                context['existing_formset'].extra = 0
        return context

    def form_valid(self, form):
        valid = super().form_valid(form)
        context = self.get_context_data()
        if context['new_formset'].is_valid() and context['existing_formset'].is_valid():
            context['new_formset'].save()
            context['existing_formset'].save()
            os.remove(settings.BASE_DIR / "media" / "domain" / "topics.xls")
        else:
            return super(TopicsFileCheckView, self).form_invalid(form)
        return valid

    def get_success_url(self, **kwargs):
        return reverse_lazy("topics_list")


class TasksFileUploadView(LoginRequiredMixin, UserPermissionsMixin, FormView):
    access = const.PROFILE_ROLES_ADMIN
    template_name = "domain/tasks_xls_upload.html"
    form_class = FileUploadForm

    def form_valid(self, form):
        try:
            file_object = self.request.FILES.get("file")
            with open(settings.BASE_DIR / "media" / "domain" / "tasks.xls", 'wb+') as destination:
                for chunk in file_object.chunks():
                    destination.write(chunk)
            df = pd.read_excel(settings.BASE_DIR / "media" / "domain" / "tasks.xls")
            df.fillna('', inplace=True)
        except Exception as e:
            return super().form_invalid(form)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super(TasksFileUploadView, self).form_invalid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy("tasks_upload_check")

    def get_context_data(self, **kwargs):
        context = super(TasksFileUploadView, self).get_context_data(**kwargs)
        context['min_code'] = min(Task.objects.all().values_list('code', flat=True))
        context['max_code'] = max(Task.objects.all().values_list('code', flat=True))
        return context


class TasksFileCheckView(LoginRequiredMixin, UserPermissionsMixin, FormView):
    access = const.PROFILE_ROLES_ADMIN
    template_name = "domain/tasks_file_check.html"
    form_class = modelformset_factory(Task,
                                      fields=('code', 'topic', 'group', 'description', 'expert_level', 'learning'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_exist = True
        try:
            xls_df = pd.read_excel(settings.BASE_DIR / "media" / "domain" / "tasks.xls",
                                   index_col=False)
            xls_df.fillna('', inplace=True)
            xls_df['learning'] = xls_df['learning'].astype(bool)
            tasks = Task.objects.filter(code__in=xls_df['code'])
            db_df = pd.DataFrame(
                tasks.values_list('code', 'topic__code', 'group', 'description', 'expert_level', 'learning'),
                columns=['code', 'topic__code', 'group', 'description', 'expert_level', 'learning'])
            db_df = db_df.rename(columns={'topic__code': 'topic'})
            equals = pd.concat([xls_df[(xls_df == pd.Series(row)).all(1)] for row in db_df.to_dict('records')])
            differences = xls_df[
                ~xls_df['code'].isin(np.array(equals['code'])) & xls_df['code'].isin(np.array(db_df['code']))]
            news = xls_df[~xls_df['code'].isin(tasks.values_list('code', flat=True))]
            self.equal_rows = equals.to_dict('records')
            self.new_rows = news.to_dict('records')
            self.existing_rows = differences.to_dict('records')
        except FileNotFoundError:
            self.file_exist = False

    def get_context_data(self, **kwargs):
        context = super(TasksFileCheckView, self).get_context_data(**kwargs)
        context['file_exist'] = self.file_exist
        if self.file_exist:
            instances = Task.objects.filter(code__in=[row['code'] for row in self.existing_rows])
            context['instances'] = instances
            if not self.request.POST:
                for row in self.existing_rows:
                    row.update({"topic": Topic.objects.get(code=row['topic'])})
                context['form'] = self.form_class(queryset=instances)
                context['form'].initial = self.existing_rows
                context['form'].extra = 0
        return context

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            for row in self.new_rows:
                row.update({"topic": Topic.objects.get(code=row['topic'])})
            Task.objects.bulk_create([Task(**row) for row in self.new_rows], batch_size=len(self.new_rows))
            os.remove(settings.BASE_DIR / "media" / "domain" / "tasks.xls")

        else:
            return super(TasksFileCheckView, self).form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy("tasks_list")


class AnswersFileUploadView(LoginRequiredMixin, UserPermissionsMixin, FormView):
    access = const.PROFILE_ROLES_ADMIN
    template_name = "domain/answers_xls_upload.html"
    form_class = FileUploadForm

    def form_valid(self, form):
        try:
            file_object = self.request.FILES.get("file")
            with open(settings.BASE_DIR / "media" / "domain" / "answers.xls", 'wb+') as destination:
                for chunk in file_object.chunks():
                    destination.write(chunk)
            df = pd.read_excel(settings.BASE_DIR / "media" / "domain" / "answers.xls")
            if Answer.objects.all().exclude(code__in=df['code']).exists():
                return super().form_invalid(form)
            rows = df.to_dict('records')
            for row in rows:
                row.update({"task": Task.objects.get(code=row['task'])})
            Answer.objects.bulk_create([Answer(**row) for row in rows], batch_size=len(rows))
            os.remove(settings.BASE_DIR / "media" / "domain" / "answers.xls")
        except Exception as e:
            return super().form_invalid(form)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super(AnswersFileUploadView, self).form_invalid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy("answers_list")

    def get_context_data(self, **kwargs):
        context = super(AnswersFileUploadView, self).get_context_data(**kwargs)
        context['min_code'] = min(Answer.objects.all().values_list('code', flat=True))
        context['max_code'] = max(Answer.objects.all().values_list('code', flat=True))
        context['answer_types'] = const.ANSWER_TYPES_DOC
        return context


class TaskImagesUploadView(LoginRequiredMixin, UserPermissionsMixin, FormView):
    access = const.PROFILE_ROLES_ADMIN
    template_name = "domain/task_images_upload.html"
    form_class = FileUploadForm

    def form_valid(self, form):
        try:
            file_object = self.request.FILES.get("file")
            with open(settings.BASE_DIR / "media" / "domain" / "images.zip", 'wb+') as destination:
                for chunk in file_object.chunks():
                    destination.write(chunk)
            arc = zipfile.ZipFile(settings.BASE_DIR / "media" / "domain" / "images.zip")
            temp_dir = settings.BASE_DIR / "media" / "domain" / "images_temp"
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            arc.extractall(temp_dir)
            arc.close()
            for d in next(os.walk(temp_dir))[1]:
                for f in next(os.walk(temp_dir / d))[2]:
                    task_code = f.split('.')[0]
                    if Task.objects.filter(code=task_code).exists():
                        task = Task.objects.get(code=task_code)
                        task.image.save(f, content=File(open(temp_dir/d/f, 'rb')))
                        task.save()
            rmtree(temp_dir)
            os.remove(settings.BASE_DIR / "media" / "domain" / "images.zip")
        except Exception as e:
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy("tasks_list")


class ModerationTasksListView(LoginRequiredMixin, UserPermissionsMixin, ListView):
    access = const.PROFILE_ROLES_TECH
    template_name = 'domain/moderation_tasks_list.html'
    model = Task
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(moderation_status__in=[const.TASK_MODERATION_STATUS_PROCESS,
                                                          const.TASK_MODERATION_STATUS_CHECKED])


class TaskModerationView(LoginRequiredMixin, UserPermissionsMixin, RedirectView):
    access = const.PROFILE_ROLES_TECH

    def get_redirect_url(self, *args, **kwargs):
        task = get_object_or_404(Task, code=self.kwargs['code'])
        task.moderation_status = const.TASK_MODERATION_STATUS_CHECKED
        task.save()
        return reverse_lazy('moderation_tasks_list')
