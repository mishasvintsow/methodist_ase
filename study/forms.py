from django.forms import ModelMultipleChoiceField, CheckboxSelectMultiple, ModelForm, inlineformset_factory, \
    HiddenInput

import const
from domain.models import Topic
from lk.models import Student
from .models import Test, Unit, Module, Item


class ProgramEditForm(ModelForm):
    class Meta:
        model = Student
        fields = ['grade']

    def __init__(self, SID, *args, **kwargs):
        super(ProgramEditForm, self).__init__(*args, **kwargs)
        self.fields['topics'] = ModelMultipleChoiceField(widget=CheckboxSelectMultiple(),
                                                         queryset=Topic.objects.all(),
                                                         initial=Module.objects.filter(student__SID=SID).values_list(
                                                             'topic__id', flat=True))


class ModuleUpdateForm(ModelForm):
    class Meta:
        model = Module
        fields = ['status', 'order']


ProgramUpdateFormSet = inlineformset_factory(Student, Module, form=ModuleUpdateForm, extra=0, can_delete=False)


class TestCreateForm(ModelForm):
    class Meta:
        model = Test
        fields = ['TID', 'student', 'time_close', 'duration', 'min_item', 'dev']

    def __init__(self, *args, **kwargs):
        super(TestCreateForm, self).__init__(*args, **kwargs)
        self.fields['TID'].widget.attrs['readonly'] = True
        self.fields['student'].widget = HiddenInput()


class UnitUpdateForm(ModelForm):
    class Meta:
        model = Unit
        fields = ['status', 'duration', 'order', 'min_item']


TestUnitsUpdateFormSet = inlineformset_factory(Test, Unit, form=UnitUpdateForm, extra=0, can_delete=False)


class TestUnitsEditForm(ModelForm):
    class Meta:
        model = Test
        fields = []

    def __init__(self, TID, *args, **kwargs):
        super(TestUnitsEditForm, self).__init__(*args, **kwargs)
        test = Test.objects.get(TID=TID)
        self.fields['modules'] = ModelMultipleChoiceField(widget=CheckboxSelectMultiple(),
                                                          queryset=Module.objects.filter(student=test.student),
                                                          initial=Unit.objects.filter(test=test).values_list(
                                                              'module__id', flat=True),
                                                          label="Модули")


class ItemSolveForm(ModelForm):
    class Meta:
        model = Item
        fields = ['response']

    def __init__(self, IID, *args, **kwargs):
        super(ItemSolveForm, self).__init__(*args, **kwargs)
        self.item = Item.objects.get(IID=IID)

    def clean(self):
        cleaned_data = super().clean()
        response = cleaned_data.get("response")
        result, errors = self.item.task.check_valid(response)
        if errors:
            self.item.attempts += 1
            self.item.save()
            if self.item.attempts <= 3:
                self.add_error(None, '\n'.join([const.ANSWER_ERRORS[e] for e in errors]))
        return cleaned_data
