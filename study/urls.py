from django.urls import path

from .views import TestsListView, TestDetailView, TestCreateView, ProgramDetailView, ProgramEditView, ProgramUpdateView, \
    TestUnitsUpdateView, TestUnitsEditView, OpenTestView, StudentTestsListView, StudentTestStartView, \
    StudentTestRunView, StudentItemRightView, StudentItemClearView, StudentItemUnclearView, StudentItemDifficultView, \
    StudentTestResultView, StudentTestDetailView, StudentProgramDetailView, StudentPracticeDetailView, \
    StudentTestCompleteView, TestResultView, ModuleItemsReworkListView, RefreshStudentParamsView, ItemReworkedView, \
    ItemReviewValidView, ItemToModerationView, ModuleDetailView, ModuleMakePlotsView, StudentModuleDetailView

urlpatterns = [
    path('admin/students/<int:SID>/program', ProgramDetailView.as_view(), name='program_detail'),
    path('admin/students/<int:SID>/program/edit', ProgramEditView.as_view(), name='program_edit'),
    path('admin/students/<int:SID>/program/update', ProgramUpdateView.as_view(), name='program_update'),
    path('admin/students/<int:SID>/tests', TestsListView.as_view(), name='tests_list'),
    path('admin/students/<int:SID>/tests/add', TestCreateView.as_view(), name='test_create'),
    path('admin/students/<int:SID>/refresh', RefreshStudentParamsView.as_view(), name='refresh_params'),
    path('admin/program/<int:MID>', ModuleDetailView.as_view(), name='module_detail'),
    path('admin/program/<int:MID>/items/rework', ModuleItemsReworkListView.as_view(), name='module_items_rework_list'),
    path('admin/tests/<int:TID>', TestDetailView.as_view(), name='test_detail'),
    path('admin/tests/<int:TID>/update', TestUnitsUpdateView.as_view(), name='test_units_update'),
    path('admin/tests/<int:TID>/edit', TestUnitsEditView.as_view(), name='test_units_edit'),
    path('admin/tests/<int:TID>/open', OpenTestView.as_view(), name='test_open'),
    path('admin/tests/<int:TID>/result', TestResultView.as_view(), name='test_result'),
    path('admin/items/<int:IID>/rework', ItemReworkedView.as_view(), name='item_rework'),
    path('admin/items/<int:IID>/review', ItemReviewValidView.as_view(), name='item_review_valid'),
    path('admin/items/<int:IID>/moderation', ItemToModerationView.as_view(), name='item_to_moderation'),
    path('program', StudentProgramDetailView.as_view(), name='student_program_detail'),
    path('program/<int:MID>/make_plots', ModuleMakePlotsView.as_view(), name='module_make_plots'),
    path('program/<int:MID>', StudentModuleDetailView.as_view(), name='student_module_detail'),
    path('program/<int:MID>/practice', StudentPracticeDetailView.as_view(), name='student_practice_start'),
    path('tests', StudentTestsListView.as_view(), name='student_tests_list'),
    path('tests/<int:TID>', StudentTestDetailView.as_view(), name='student_test_detail'),
    path('tests/<int:TID>/start', StudentTestStartView.as_view(), name='student_test_start'),
    path('tests/<int:TID>/run', StudentTestRunView.as_view(), name='student_test_run'),
    path('tests/<int:TID>/complete', StudentTestCompleteView.as_view(), name='student_test_complete'),
    path('tests/<int:TID>/result', StudentTestResultView.as_view(), name='student_test_result'),
    path('item/<int:IID>/right', StudentItemRightView.as_view(), name='student_item_right'),
    path('item/<int:IID>/clear', StudentItemClearView.as_view(), name='student_item_clear'),
    path('item/<int:IID>/unclear', StudentItemUnclearView.as_view(), name='student_item_unclear'),
    path('item/<int:IID>/difficult', StudentItemDifficultView.as_view(), name='student_item_difficult')

]
