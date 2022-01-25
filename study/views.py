from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import UpdateView, CreateView, DetailView, RedirectView
from django.views.generic.list import ListView

import const
from lk.models import Student
from mixins import UserPermissionsMixin, StudentPermissionsMixin
from study.forms import ProgramEditForm, ProgramUpdateFormSet, TestCreateForm, \
    TestUnitsUpdateFormSet, TestUnitsEditForm, ItemSolveForm
from study.models import Module, Test, Unit, Item


class ProgramDetailView(LoginRequiredMixin, UserPermissionsMixin, ListView):
    access = const.PROFILE_ROLES_MODERATOR
    template_name = "study/program_detail.html"
    model = Module
    context_object_name = 'program'

    def __init__(self, **kwargs):
        super(ProgramDetailView, self).__init__(**kwargs)
        self.student = None

    def get_queryset(self):
        student = get_object_or_404(Student, SID=self.kwargs['SID'])
        self.student = student
        return Module.objects.filter(student=student).order_by('order')

    def get_context_data(self, **kwargs):
        context = super(ProgramDetailView, self).get_context_data(**kwargs)
        context['student'] = self.student
        self.student.check_tests()
        return context


class ProgramUpdateView(LoginRequiredMixin, UserPermissionsMixin, UpdateView):
    access = const.PROFILE_ROLES_ADMIN
    template_name = "study/program_update.html"
    model = Student
    context_object_name = 'student'
    fields = ['grade']

    def get_object(self, queryset=None):
        return get_object_or_404(Student, SID=self.kwargs['SID'])

    def get_context_data(self, **kwargs):
        context = super(ProgramUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ProgramUpdateFormSet(self.request.POST, instance=self.object)
            context['formset'].full_clean()
        else:
            context['formset'] = ProgramUpdateFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if form.is_valid() and formset.is_valid():
            response = super().form_valid(form)
            formset.save()
            return response
        else:
            return super().form_invalid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy("program_detail", args=(self.object.SID,))


class ProgramEditView(LoginRequiredMixin, UserPermissionsMixin, UpdateView):
    access = const.PROFILE_ROLES_ADMIN
    template_name = "study/program_edit.html"
    model = Student
    form_class = ProgramEditForm

    def get_object(self, **kwargs):
        return get_object_or_404(Student, SID=self.kwargs['SID'])

    def get_form_kwargs(self):
        kwargs = super(ProgramEditView, self).get_form_kwargs()
        kwargs['SID'] = self.object.SID
        return kwargs

    def form_valid(self, form):
        if form.is_valid():
            topics_in = form.cleaned_data['topics']
            Module.objects.filter(student=self.object).exclude(topic__in=topics_in).update(
                status=const.MODULE_STATUS_DELETED)
            for i, module in enumerate(Module.objects.filter(student=self.object).order_by('order')):
                module.order = i + 1
                module.save()

            i = Module.objects.filter(student=self.object).count()
            for topic in topics_in:
                if not Module.objects.filter(student=self.object, topic=topic).exists():
                    Module.objects.create(student=self.object,
                                          topic=topic,
                                          MID=Module.objects.aggregate(max_MID=Max('MID'))['max_MID'] + 1,
                                          order=i + 1)
                    i += 1
            return super().form_valid(form)
        else:
            return super().form_invalid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy("program_update", args=(self.object.SID,))


class TestsListView(LoginRequiredMixin, UserPermissionsMixin, ListView):
    access = const.PROFILE_ROLES_MODERATOR
    template_name = 'study/tests_list.html'
    model = Test
    context_object_name = 'tests'

    def get_queryset(self):
        student = get_object_or_404(Student, SID=self.kwargs['SID'])
        return Test.objects.filter(student=student)

    def get_context_data(self, **kwargs):
        context = super(TestsListView, self).get_context_data(**kwargs)
        student = get_object_or_404(Student, SID=self.kwargs['SID'])
        context['student'] = student
        context['tests_future'] = self.get_queryset().filter(status__in=[const.TEST_STATUS_OPENED,
                                                                         const.TEST_STATUS_CREATED,
                                                                         const.TEST_STATUS_STARTED],
                                                             practice=False).order_by('time_close')
        context['tests_pass'] = self.get_queryset().filter(status__in=[const.TEST_STATUS_FINISHED,
                                                                       const.TEST_STATUS_CLOSED],
                                                           practice=False).order_by('-time_create')
        context['practices'] = self.get_queryset().filter(practice=True)
        student.check_tests()
        return context


class TestDetailView(LoginRequiredMixin, UserPermissionsMixin, DetailView):
    access = const.PROFILE_ROLES_MODERATOR
    template_name = 'study/test_detail.html'
    model = Test
    context_object_name = 'test'

    def get_object(self, **kwargs):
        return get_object_or_404(Test, TID=self.kwargs['TID'])

    def get_context_data(self, **kwargs):
        context = super(TestDetailView, self).get_context_data(**kwargs)
        context['units'] = Unit.objects.filter(test=self.object)
        return context


class TestResultView(LoginRequiredMixin, UserPermissionsMixin, DetailView):
    access = const.PROFILE_ROLES_MODERATOR
    template_name = 'study/test_result.html'
    model = Test
    context_object_name = 'test'

    def get_object(self, **kwargs):
        return get_object_or_404(Test, TID=self.kwargs['TID'])

    def get_context_data(self, **kwargs):
        context = super(TestResultView, self).get_context_data(**kwargs)
        context['units_items'] = [(unit, Item.objects.filter(unit=unit)) for unit in
                                  Unit.objects.filter(test=self.object)]
        return context


class TestCreateView(LoginRequiredMixin, UserPermissionsMixin, CreateView):
    access = const.PROFILE_ROLES_MODERATOR
    template_name = 'study/test_create.html'
    model = Test
    form_class = TestCreateForm

    def get_initial(self):
        initial = super(TestCreateView, self).get_initial()
        initial['TID'] = Test.objects.aggregate(max_TID=Max('TID'))['max_TID'] + 1
        initial['student'] = get_object_or_404(Student, SID=self.kwargs['SID'])
        initial['time_close'] = timezone.now() + timedelta(days=7)
        return initial

    def form_valid(self, form):
        if form.is_valid():
            test = form.save()
            for i, module in enumerate(Module.objects.filter(student=test.student,
                                                             status__in=[const.MODULE_STATUS_REPEATING,
                                                                         const.MODULE_STATUS_LEARNING]).order_by(
                'order')):
                Unit.objects.create(UID=Unit.objects.aggregate(max_UID=Max('UID'))['max_UID'] + 1,
                                    test=test,
                                    module=module,
                                    order=i + 1,
                                    status=module.status,
                                    duration=test.duration,
                                    min_item=test.min_item)
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('test_units_update', args=(self.object.TID,))


class TestUnitsUpdateView(LoginRequiredMixin, UserPermissionsMixin, UpdateView):
    access = const.PROFILE_ROLES_MODERATOR
    template_name = 'study/test_units_update.html'
    model = Test
    context_object_name = 'test'
    fields = ['time_close', 'dev']

    def get_object(self, **kwargs):
        return get_object_or_404(Test, TID=self.kwargs['TID'])

    def get_context_data(self, **kwargs):
        context = super(TestUnitsUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = TestUnitsUpdateFormSet(self.request.POST, instance=self.object)
            context['formset'].full_clean()
        else:
            context['formset'] = TestUnitsUpdateFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if form.is_valid() and formset.is_valid():
            response = super().form_valid(form)
            formset.save()
            return response
        else:
            return super().form_invalid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('test_detail', args=(self.object.TID,))


class TestUnitsEditView(LoginRequiredMixin, UserPermissionsMixin, UpdateView):
    access = const.PROFILE_ROLES_MODERATOR
    template_name = "study/test_units_edit.html"
    model = Test
    form_class = TestUnitsEditForm

    def get_object(self, **kwargs):
        return get_object_or_404(Test, TID=self.kwargs['TID'])

    def get_form_kwargs(self):
        kwargs = super(TestUnitsEditView, self).get_form_kwargs()
        kwargs['TID'] = self.object.TID
        return kwargs

    def form_valid(self, form):
        if form.is_valid():
            modules_in = form.cleaned_data['modules']
            Unit.objects.filter(test=self.object).exclude(module__in=modules_in).delete()
            for i, unit in enumerate(Unit.objects.filter(test=self.object).order_by('order')):
                unit.order = i + 1
                unit.save()

            i = Unit.objects.filter(test=self.object).count()
            for module in modules_in:
                if not Unit.objects.filter(test=self.object, module=module).exists():
                    Unit.objects.create(test=self.object,
                                        module=module,
                                        UID=Unit.objects.aggregate(max_UID=Max('UID'))['max_UID'] + 1,
                                        order=i + 1,
                                        duration=self.object.duration,
                                        min_item=self.object.min_item)
                    i += 1
            return super().form_valid(form)
        else:
            return super().form_invalid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy("test_units_update", args=(self.object.TID,))


class StudentProgramDetailView(LoginRequiredMixin, StudentPermissionsMixin, ListView):
    template_name = "study/student_program_detail.html"
    model = Module
    context_object_name = 'program'

    def get_queryset(self):
        student = get_object_or_404(Student, SID=self.request.user.student.SID)
        student.check_tests()
        return Module.objects.filter(student=student).order_by('order')


class ModuleDetailView(LoginRequiredMixin, UserPermissionsMixin, DetailView):
    access = const.PROFILE_ROLES_MODERATOR
    template_name = "study/module_detail.html"
    model = Module
    context_object_name = 'module'

    def get_object(self, **kwargs):
        return get_object_or_404(Module, MID=self.kwargs['MID'])


class StudentModuleDetailView(LoginRequiredMixin, StudentPermissionsMixin, DetailView):
    template_name = "study/student_module_detail.html"
    model = Module
    context_object_name = 'module'

    def get_object(self, **kwargs):
        module = get_object_or_404(Module, MID=self.kwargs['MID'])
        return module


class ModuleMakePlotsView(LoginRequiredMixin, UserPermissionsMixin, StudentPermissionsMixin, RedirectView):
    access = const.PROFILE_ROLES_ALL

    def get_redirect_url(self, *args, **kwargs):
        module = get_object_or_404(Module, MID=self.kwargs['MID'])
        module.moduleparam.make_plots()
        if self.request.user.student is not None and self.request.user.student == module.student:
            return reverse('student_module_detail', args=(module.MID,))
        else:
            return reverse('module_detail', args=(module.MID,))


class ModuleItemsReworkListView(LoginRequiredMixin, UserPermissionsMixin, ListView):
    access = const.PROFILE_ROLES_MODERATOR
    template_name = "study/module_items_rework_list.html"
    model = Item
    context_object_name = 'items'

    def get_queryset(self):
        module = get_object_or_404(Module, MID=self.kwargs['MID'])
        return Item.objects.filter(unit__module=module).exclude(analysis=const.ITEM_ANALYSIS_NONE)

    def get_context_data(self, **kwargs):
        context = super(ModuleItemsReworkListView, self).get_context_data(**kwargs)
        items = self.get_queryset()
        context['items_groups'] = [
            (const.ITEM_STATUSES[const.ITEM_STATUS_DIFFICULT], items.filter(status=const.ITEM_STATUS_DIFFICULT)),
            (const.ITEM_STATUSES[const.ITEM_STATUS_UNCLEAR], items.filter(status=const.ITEM_STATUS_UNCLEAR)),
            (const.ITEM_STATUSES[const.ITEM_STATUS_CLEAR], items.filter(status=const.ITEM_STATUS_CLEAR)),
            (const.ITEM_STATUSES[const.ITEM_STATUS_MODERATION], items.filter(status=const.ITEM_STATUS_MODERATION))]
        return context


class RefreshStudentParamsView(LoginRequiredMixin, UserPermissionsMixin, RedirectView):
    access = const.PROFILE_ROLES_MODERATOR

    def get_redirect_url(self, *args, **kwargs):
        student = get_object_or_404(Student, SID=self.kwargs['SID'])
        for unit in Unit.objects.filter(module__student=student):
            unit.unitparam.refresh_params()
        for module in Module.objects.filter(student=student):
            module.moduleparam.refresh_params()
        student.studentparam.refresh_params()
        return reverse_lazy('program_detail', args=(student.SID,))


class ItemReworkedView(LoginRequiredMixin, UserPermissionsMixin, RedirectView):
    access = const.PROFILE_ROLES_MODERATOR

    def get_redirect_url(self, *args, **kwargs):
        item = get_object_or_404(Item, IID=self.kwargs['IID'])
        item.analysis = const.ITEM_ANALYSIS_DONE
        item.save()
        return reverse_lazy('module_items_rework_list', args=(item.unit.module.MID,))


class ItemReviewValidView(LoginRequiredMixin, UserPermissionsMixin, RedirectView):
    access = const.PROFILE_ROLES_MODERATOR

    def get_redirect_url(self, *args, **kwargs):
        item = get_object_or_404(Item, IID=self.kwargs['IID'])
        item.valid = True
        item.analysis = const.ITEM_ANALYSIS_DONE
        item.save()
        return reverse_lazy('module_items_rework_list', args=(item.unit.module.MID,))


class ItemToModerationView(LoginRequiredMixin, UserPermissionsMixin, RedirectView):
    access = const.PROFILE_ROLES_MODERATOR

    def get_redirect_url(self, *args, **kwargs):
        item = get_object_or_404(Item, IID=self.kwargs['IID'])
        item.analysis = const.ITEM_ANALYSIS_DONE
        item.status = const.ITEM_STATUS_MODERATION
        item.save()
        item.task.moderation_status = const.TASK_MODERATION_STATUS_PROCESS
        item.task.save()
        return reverse_lazy('module_items_rework_list', args=(item.unit.module.MID,))


class OpenTestView(LoginRequiredMixin, UserPermissionsMixin, RedirectView):
    access = const.PROFILE_ROLES_MODERATOR

    def get_redirect_url(self, *args, **kwargs):
        test = get_object_or_404(Test, TID=self.kwargs['TID'])
        test.time_open = timezone.now()
        test.status = const.TEST_STATUS_OPENED
        test.save()
        return reverse_lazy('test_detail', args=(test.TID,))


class StudentTestsListView(LoginRequiredMixin, StudentPermissionsMixin, ListView):
    template_name = 'study/student_tests_list.html'
    model = Test
    context_object_name = 'tests'

    def get_queryset(self):
        student = get_object_or_404(Student, user=self.request.user)
        student.check_tests()
        return Test.objects.filter(student=student)

    def get_context_data(self, **kwargs):
        context = super(StudentTestsListView, self).get_context_data(**kwargs)
        context['tests_future'] = self.get_queryset().filter(status__in=[const.TEST_STATUS_OPENED,
                                                                         const.TEST_STATUS_STARTED],
                                                             practice=False).order_by('time_close')
        context['tests_pass'] = self.get_queryset().filter(status__in=[const.TEST_STATUS_FINISHED,
                                                                       const.TEST_STATUS_CLOSED],
                                                           practice=False).order_by('-time_create')
        context['practices'] = self.get_queryset().filter(practice=True)
        return context


class StudentTestDetailView(LoginRequiredMixin, StudentPermissionsMixin, DetailView):
    template_name = 'study/student_test_detail.html'
    model = Test
    context_object_name = 'test'

    def get_object(self, **kwargs):
        test = get_object_or_404(Test, TID=self.kwargs['TID'])
        return test

    def get_context_data(self, **kwargs):
        context = super(StudentTestDetailView, self).get_context_data(**kwargs)
        context['units'] = Unit.objects.filter(test=self.object)
        return context


class StudentTestResultView(LoginRequiredMixin, StudentPermissionsMixin, DetailView):
    template_name = 'study/student_test_result.html'
    model = Test
    context_object_name = 'test'

    def get_object(self, **kwargs):
        test = get_object_or_404(Test, TID=self.kwargs['TID'])
        return test

    def get_context_data(self, **kwargs):
        context = super(StudentTestResultView, self).get_context_data(**kwargs)
        context['units_items'] = [(unit, Item.objects.filter(unit=unit)) for unit in
                                  Unit.objects.filter(test=self.object)]
        print(context['units_items'])
        return context


class StudentTestStartView(LoginRequiredMixin, StudentPermissionsMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        test = get_object_or_404(Test, TID=self.kwargs['TID'])
        if test.status == const.TEST_STATUS_OPENED:
            if test.run() is not None:
                return reverse_lazy('student_test_run', args=(test.TID,))
            else:
                return reverse_lazy('student_test_result', args=(test.TID,))
        elif test.status == const.TEST_STATUS_STARTED:
            return reverse_lazy('student_test_run', args=(test.TID,))
        else:
            return reverse_lazy('student_test_result', args=(test.TID,))


class StudentPracticeDetailView(LoginRequiredMixin, StudentPermissionsMixin, DetailView):
    template_name = 'study/student_test_detail.html'
    model = Test
    context_object_name = 'test'

    def get_object(self, **kwargs):
        module = get_object_or_404(Module, MID=self.kwargs['MID'])
        if Test.objects.filter(student=module.student,
                               practice=True,
                               status=const.TEST_STATUS_STARTED).exists():
            return Test.objects.filter(student=module.student,
                                       practice=True,
                                       status=const.TEST_STATUS_STARTED).first()
        else:
            test = Test.objects.create(TID=Test.objects.aggregate(max_TID=Max('TID'))['max_TID'] + 1,
                                       student=module.student,
                                       time_open=timezone.now(),
                                       time_close=timezone.now() + timedelta(hours=1),
                                       duration=30,
                                       min_item=0,
                                       practice=True)
            Unit.objects.create(UID=Unit.objects.aggregate(max_UID=Max('UID'))['max_UID'] + 1,
                                test=test,
                                module=module,
                                status=const.UNIT_STATUS_REPEATING,
                                order=1,
                                duration=30,
                                min_item=0)
            test.run()
            return test

    def get_context_data(self, **kwargs):
        context = super(StudentPracticeDetailView, self).get_context_data(**kwargs)
        context['units'] = Unit.objects.filter(test=self.object)
        context['items'] = Item.objects.filter(unit__test=self.object)
        return context


class StudentTestCompleteView(LoginRequiredMixin, StudentPermissionsMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        test = get_object_or_404(Test, TID=self.kwargs['TID'])
        Item.objects.filter(unit__test=test,
                            status=const.ITEM_STATUS_NORESPONSE).delete()
        Unit.objects.filter(test=test).first().complete()
        test.complete()
        return reverse_lazy('student_test_result', args=(test.TID,))


class StudentTestRunView(LoginRequiredMixin, StudentPermissionsMixin, UpdateView):
    template_name = 'study/student_test_run.html'
    model = Item
    form_class = ItemSolveForm
    context_object_name = 'item'

    def get_object(self, **kwargs):
        test = Test.objects.get(TID=self.kwargs['TID'])
        unit = test.get_active_unit()
        item = unit.get_active_item()
        if item.time_start is None:
            item.run()
        try:
            if item.valid is not None:
                self.template_name = 'study/student_test_item_check.html'
            return item
        except AttributeError:
            raise Http404

    def get_form_kwargs(self):
        kwargs = super(StudentTestRunView, self).get_form_kwargs()
        kwargs['IID'] = self.object.IID
        return kwargs

    def form_valid(self, form):
        item = form.save()
        item.complete()
        return super().form_valid(form)

    def get_success_url(self):
        item = self.object
        if item.attempts >= 3:
            item.complete_incorrect()
            item.unit.test.choose_unit()
            if item.unit.test.add_item() is not None:
                return reverse_lazy('student_test_run', args=(item.unit.test.TID,))
            else:
                item.unit.test.complete()
                return reverse_lazy('student_test_result', args=(item.unit.test.TID,))
        return reverse_lazy('student_test_run', args=(item.unit.test.TID,))

    def get_context_data(self, **kwargs):
        context = super(StudentTestRunView, self).get_context_data(**kwargs)
        items = Item.objects.filter(unit__test__TID=self.kwargs['TID'])
        m, s = divmod(self.object.unit.time_left(), 60)
        print(m, s)
        context['minutes'] = int(m)
        context['seconds'] = int(s)
        context['items'] = items
        context['task_left'] = int(self.object.unit.min_item - items.filter(unit=self.object.unit).exclude(
            status__in=[const.ITEM_STATUS_INCORRECT, const.ITEM_STATUS_NORESPONSE]).count() + 1)
        return context


class StudentItemRightView(LoginRequiredMixin, StudentPermissionsMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        item = get_object_or_404(Item, IID=self.kwargs['IID'])
        item.status = const.ITEM_STATUS_RIGHT
        item.save()
        item.unit.test.choose_unit()
        if item.unit.test.add_item() is not None:
            return reverse_lazy('student_test_run', args=(item.unit.test.TID,))
        else:
            item.unit.test.complete()
            return reverse_lazy('student_test_result', args=(item.unit.test.TID,))


class StudentItemClearView(LoginRequiredMixin, StudentPermissionsMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        item = get_object_or_404(Item, IID=self.kwargs['IID'])
        item.status = const.ITEM_STATUS_CLEAR
        item.analysis = const.ITEM_ANALYSIS_TODO
        item.save()
        item.unit.test.choose_unit()
        if item.unit.test.add_item() is not None:
            return reverse_lazy('student_test_run', args=(item.unit.test.TID,))
        else:
            item.unit.test.complete()
            return reverse_lazy('student_test_result', args=(item.unit.test.TID,))


class StudentItemUnclearView(LoginRequiredMixin, StudentPermissionsMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        item = get_object_or_404(Item, IID=self.kwargs['IID'])
        item.status = const.ITEM_STATUS_UNCLEAR
        item.analysis = const.ITEM_ANALYSIS_TODO
        item.save()
        item.unit.test.choose_unit()
        if item.unit.test.add_item() is not None:
            return reverse_lazy('student_test_run', args=(item.unit.test.TID,))
        else:
            item.unit.test.complete()
            return reverse_lazy('student_test_result', args=(item.unit.test.TID,))


class StudentItemDifficultView(LoginRequiredMixin, StudentPermissionsMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        item = get_object_or_404(Item, IID=self.kwargs['IID'])
        item.complete_difficult()
        item.unit.test.choose_unit()
        if item.unit.test.add_item() is not None:
            return reverse_lazy('student_test_run', args=(item.unit.test.TID,))
        else:
            item.unit.test.complete()
            return reverse_lazy('student_test_result', args=(item.unit.test.TID,))
