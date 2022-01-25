from django.core.exceptions import ValidationError
from django.forms import Form, ModelForm, CharField, FileField, HiddenInput
from django.forms.models import inlineformset_factory
from django.utils.translation import gettext as _

import answers
import const
from domain.models import Course, Topic, Task, Answer


class CourseCreateUpdateForm(ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'name']


class TopicCreateUpdateForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['code', 'name', 'grade', 'course']

    def __init__(self, hidden_course=False, **kwargs):
        super(TopicCreateUpdateForm, self).__init__(**kwargs)
        if hidden_course:
            self.fields['course'].widget = HiddenInput()


class TaskCreateUpdateForm(ModelForm):
    class Meta:
        model = Task
        fields = ['code', 'topic', 'group', 'description', 'expert_level', 'learning', 'image']


class TaskForSetForm(ModelForm):
    class Meta:
        model = Task
        fields = ['code', 'topic', 'group', 'description', 'expert_level', 'learning']


class TaskSolveForm(ModelForm):
    response = CharField()

    class Meta:
        model = Task
        fields = ['code']

    def __init__(self, *args, **kwargs):
        super(TaskSolveForm, self).__init__(*args, **kwargs)
        self.fields['code'].widget.attrs.update({'readonly': True})
        self.fields['code'].initial = self.instance.code

    def clean(self):
        cleaned_data = super().clean()
        response = cleaned_data.get("response")
        result, errors = self.instance.check_valid(response)
        if errors:
            self.add_error(None, '\n'.join([const.ANSWER_ERRORS[e] for e in errors]))
        elif not result:
            self.add_error(None, "Неправильный ответ")
        return cleaned_data


class TaskPlugForm(ModelForm):
    class Meta:
        model = Task
        fields = ['code']

    def __init__(self, *args, **kwargs):
        super(TaskPlugForm, self).__init__(*args, **kwargs)
        self.fields['code'].widget.attrs.update({'readonly': True})


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['code', 'answer_type', 'text']

    def clean(self):
        cleaned_data = super().clean()
        answer_type = cleaned_data.get("answer_type")
        text = cleaned_data.get("text")

        if answer_type and text:
            AnswerClass = answers.ANSWER_CLASSES[answer_type]
            answer_syntax_check = AnswerClass(text=text).syntax_check(text)

            if answer_syntax_check != const.ANSWER_ERROR_NOT:
                raise ValidationError(
                    _('Invalid syntax: %(value)s'),
                    code='invalid',
                    params={'value': const.ANSWER_ERRORS[answer_syntax_check]},
                )
        return cleaned_data


AnswersFormSet = inlineformset_factory(Task, Answer, form=AnswerForm, extra=1)
TopicsFormSet = inlineformset_factory(Course, Topic, fields=['code', 'name', 'grade'], extra=0)


class FileUploadForm(Form):
    file = FileField(label="Файл .xlsx")
