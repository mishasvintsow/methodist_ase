from django_filters import FilterSet, ChoiceFilter

import const
from lk.models import Student


class StudentsFilter(FilterSet):
    class Meta:
        model = Student
        fields = []

    homework_filter = ChoiceFilter(label="Наличие д/з", field_name='homework_filter', choices=const.FILTERS_HOMEWORK,
                                   empty_label="Все ученики")
    analysis_filter = ChoiceFilter(label="Разбор заданий", field_name='analysis_filter', choices=const.FILTERS_ANALYSIS,
                                   empty_label="Все ученики")
    regress_filter = ChoiceFilter(label="Регресс (повторение)", field_name='regress_filter',
                                  choices=const.FILTERS_REGRESS, empty_label="Все ученики")
    learning_filter = ChoiceFilter(label="Трудности (изучение)", field_name='learning_filter',
                                   choices=const.FILTERS_LEARNING, empty_label="Все ученики")
