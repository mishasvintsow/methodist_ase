# import re
#
def par_checker(string):
    balanced = True
    index = 0
    s = []
    while index < len(string) and balanced:
        symbol = string[index]
        if symbol == "(":
            s.append(symbol)
        elif symbol == ")":
            if len(s) == 0:
                balanced = False
            else:
                s.pop()

        index = index + 1

    if balanced and len(s) == 0:
        return True
    else:
        return False


#
# TESTTASK_STATUS_RIGHT = 0
# TESTTASK_STATUS_CLEAR = 1
# TESTTASK_STATUS_UNCLEAR = 2
# TESTTASK_STATUS_DIFFICULT = 3
# TESTTASK_STATUS_MODERATION = 4
#
# TESTTASK_STATUSES = {
#    TESTTASK_STATUS_RIGHT : "Следующее задание",
#    TESTTASK_STATUS_CLEAR : "Ясно",
#    TESTTASK_STATUS_UNCLEAR : "Не понятно",
#    TESTTASK_STATUS_DIFFICULT : "Затрудняюсь",
#    TESTTASK_STATUS_MODERATION : "Модерация"
# }
#
# TESTTASK_STATUSES_DISPLAY = list(TESTTASK_STATUSES.items())


# PROFILE_ROLES_ACCESS = {
#    PROFILE_ROLE_ROOT : 'Суперпользователь',
#    PROFILE_ROLES_ADMIN : 'Администратор: суперпользователь/методист',
#    PROFILE_ROLES_MODERATOR : 'Модераторы: суперпользователь/методист/учитель',
#    PROFILE_ROLES_STUFF : 'Сотрудники: суперпользователь/методист/учитель/аудитор',
#    PROFILE_ROLE_AUDITOR : 'Аудитор',
#    PROFILE_ROLE_STUDENT : 'Студент',
#    PROFILE_ROLES_ALL : 'Все пользователи',
#    PROFILE_ROLE_ANON : 'Аноним',
# }
#
# PROFILE_ROLES_ACCESS_DISPLAY = list(PROFILE_ROLES_ACCESS.items())
#
#


# TOPIC_STATUS_REPEAT = 'r'
# TOPIC_STATUS_CURRENT = 'c'
# TOPIC_STATUS_MAIN = 'm'
# TOPIC_STATUS_DELETED = 'd'
#
# TOPIC_STATUSES = {
#    TOPIC_STATUS_REPEAT : 'Повторение',
#    TOPIC_STATUS_CURRENT : 'Текущая',
#    TOPIC_STATUS_MAIN : 'Не приступали',
#    TOPIC_STATUS_DELETED : 'Удалена',
# }
#
# TOPIC_STATUSES_DISPLAY = list(TOPIC_STATUSES.items())
#
#
#
#
#
# TOPIC_STATUS_ADD_REPEAT = 'ar'
# TOPIC_STATUS_ADD_CURRENT = 'ac'
# TOPIC_STATUS_ADD_MAIN = 'am'
# TOPIC_STATUS_DELETE_REPEAT = 'rd'
# TOPIC_STATUS_DELETE_CURRENT = 'cd'
# TOPIC_STATUS_DELETE_MAIN = 'md'
# TOPIC_STATUS_REPEAT_TO_CURRENT = 'rc'
# TOPIC_STATUS_REPEAT_TO_MAIN = 'rm'
# TOPIC_STATUS_CURRENT_TO_REPEAT = 'cr'
# TOPIC_STATUS_CURRENT_TO_MAIN = 'cm'
# TOPIC_STATUS_MAIN_TO_CURRENT = 'mc'
# TOPIC_STATUS_MAIN_TO_REPEAT = 'mr'
#
#
# TOPIC_STATUS_CHANGES = {
#    TOPIC_STATUS_ADD_REPEAT : 'Добавить в темы для повторения',
#    TOPIC_STATUS_ADD_CURRENT : 'Добавить в текущие темы',
#    TOPIC_STATUS_ADD_MAIN : 'Добавить в основную программу',
#    TOPIC_STATUS_DELETE_REPEAT : 'Удалить тему для повторения из программы',
#    TOPIC_STATUS_DELETE_CURRENT : 'Удалить текущую тему из программы',
#    TOPIC_STATUS_DELETE_MAIN : 'Удалить тему из основной программы',
#    TOPIC_STATUS_REPEAT_TO_CURRENT : 'Повторение -> Текущая тема',
#    TOPIC_STATUS_REPEAT_TO_MAIN : 'Повторение -> Основная программа',
#    TOPIC_STATUS_CURRENT_TO_REPEAT : 'Текущая тема -> Повторение',
#    TOPIC_STATUS_CURRENT_TO_MAIN : 'Текущая тема -> Основная программа',
#    TOPIC_STATUS_MAIN_TO_REPEAT : 'Основная программа -> Повторение',
#    TOPIC_STATUS_MAIN_TO_CURRENT : 'Основная программа -> Текущая тема',
# }
#
# TOPIC_STATUS_CHANGES_DISPLAY = list(TOPIC_STATUS_CHANGES.items())
#
#

#
#
# FEATURES = ['student_count_all',
#                'student_count_all_level',         
#                'student_count_true',              
#                'student_count_true_level',        
#                'student_progress_rel',            
#                'student_progress_rel_true_level', 
#                'student_progress_rel_all_level',  
#                'student_diff',                    
#                'student_dev',                     
#                'student_penalty',                 
#                'student_last_tt_real',
#                'stuto_count_all',               
#                'stuto_count_all_level',         
#                'stuto_count_true',              
#                'stuto_count_true_level',        
#                'stuto_progress_rel',            
#                'stuto_progress_rel_true_level', 
#                'stuto_progress_rel_all_level',  
#                'stuto_diff',                    
#                'stuto_dev',                     
#                'stuto_penalty',                 
#                'stuto_last_tt_real',
#                'test_count_all',               
#                'test_count_all_level',         
#                'test_count_true',              
#                'test_count_true_level',        
#                'test_progress_rel',            
#                'test_progress_rel_true_level', 
#                'test_progress_rel_all_level',  
#                'test_diff',                    
#                'test_dev',                     
#                'test_penalty',                 
#                'test_last_tt_real',
#                'teto_count_all',               
#                'teto_count_all_level',         
#                'teto_count_true',              
#                'teto_count_true_level',        
#                'teto_progress_rel',            
#                'teto_progress_rel_true_level', 
#                'teto_progress_rel_all_level',  
#                'teto_diff',                    
#                'teto_dev',                     
#                'teto_penalty',                 
#                'teto_last_tt_real',
#                'tt__valid']
# PREDICTED = 'task_rel_smooth_expert'

# answer_pic = {True : "/static/images/greencheck.jpg",
#              False : "/static/images/redcross.png",
#              None : "/static/images/blackques.jpg"}
#
# def plural_days(n):
#    days = ['день', 'дня', 'дней']
#    
#    if n % 10 == 1 and n % 100 != 11:
#        p = 0
#    elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
#        p = 1
#    else:
#        p = 2
#
#    return str(n) + ' ' + days[p]
#
# def plural_tasks(n):
#    tasks = ['задание', 'задания', 'заданий']
#    
#    if n % 10 == 1 and n % 100 != 11:
#        p = 0
#    elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
#        p = 1
#    else:
#        p = 2
#
#    return str(n) + ' ' + tasks[p]


import re

# app: lk

PROFILE_ROLE_ANON = 'n'
PROFILE_ROLE_AUDITOR = 'a'
PROFILE_ROLE_STUDENT = 's'
PROFILE_ROLE_TEACHER = 't'
PROFILE_ROLE_METHODIST = 'm'
PROFILE_ROLE_ROOT = 'r'

PROFILE_ROLES_ADMIN = PROFILE_ROLE_ROOT + PROFILE_ROLE_METHODIST
PROFILE_ROLES_MODERATOR = PROFILE_ROLES_ADMIN + PROFILE_ROLE_TEACHER
PROFILE_ROLES_TECH = PROFILE_ROLES_ADMIN + PROFILE_ROLE_AUDITOR
PROFILE_ROLES_STUFF = PROFILE_ROLES_MODERATOR + PROFILE_ROLE_AUDITOR
PROFILE_ROLES_ALL = PROFILE_ROLES_STUFF + PROFILE_ROLE_STUDENT

PROFILE_ROLES = {
    PROFILE_ROLE_ROOT: 'Суперпользователь',
    PROFILE_ROLE_METHODIST: 'Методист',
    PROFILE_ROLE_TEACHER: 'Учитель',
    PROFILE_ROLE_AUDITOR: 'Аудитор',
    PROFILE_ROLE_STUDENT: 'Студент',
    PROFILE_ROLE_ANON: 'Аноним',
}

PROFILE_ROLES_DISPLAY = list(PROFILE_ROLES.items())

GRADES = [n for n in range(5, 12)]
GRADES_DISPLAY = [(n, str(n)) for n in GRADES]

# app: domain

TASK_MODERATION_STATUS_UNCHECKED = 'u'
TASK_MODERATION_STATUS_PROCESS = 'p'
TASK_MODERATION_STATUS_CHECKED = 'c'

TASK_MODERATION_STATUSES = {
    TASK_MODERATION_STATUS_UNCHECKED: "Не проверено",
    TASK_MODERATION_STATUS_PROCESS: "В процессе",
    TASK_MODERATION_STATUS_CHECKED: "Проверено"
}

TASK_MODERATION_STATUSES_DISPLAY = list(TASK_MODERATION_STATUSES.items())

EXPERT_LEVEL_LOW = 0
EXPERT_LEVEL_MEDIUM = 1
EXPERT_LEVEL_HIGH = 2

EXPERT_LEVELS = {EXPERT_LEVEL_LOW: 'Низкий',
                 EXPERT_LEVEL_MEDIUM: 'Средний',
                 EXPERT_LEVEL_HIGH: 'Высокий'}

EXPERT_LEVELS_DISPLAY = list(EXPERT_LEVELS.items())

TASK_LEVEL_INITIAL = {EXPERT_LEVEL_LOW: 0.17163402715560913,
                      EXPERT_LEVEL_MEDIUM: 0.38676645293062106,
                      EXPERT_LEVEL_HIGH: 0.5866154166562821}

ANSWER_TYPE_FREE = 'f'
ANSWER_TYPE_CHOICE = 'c'
ANSWER_TYPE_MATHEXP = 'x'
ANSWER_TYPE_MATHWRONG = 'w'
ANSWER_TYPE_POINT = 'p'
ANSWER_TYPE_YESNO = 'y'
ANSWER_TYPE_INTERVAL = 'i'
ANSWER_TYPE_INEQUALITY = 'n'
ANSWER_TYPE_EQUALITY = 'e'
ANSWER_TYPE_CYRILLIC = 'r'
ANSWER_TYPE_MATCH = 'm'
ANSWER_TYPE_DELETE = 'd'

ANSWER_TYPES_DOC = {
    ANSWER_TYPE_FREE: "Произвольный ответ",
    ANSWER_TYPE_CHOICE: "Выбор",
    ANSWER_TYPE_MATHEXP: "Математическое выражение",
    ANSWER_TYPE_POINT: "Точка",
    ANSWER_TYPE_YESNO: "Да/нет",
    ANSWER_TYPE_INTERVAL: "Интервал",
    ANSWER_TYPE_INEQUALITY: "Неравенство",
    ANSWER_TYPE_EQUALITY: "Равенство",
    ANSWER_TYPE_CYRILLIC: "Текст (кириллица)",
    ANSWER_TYPE_MATCH: "Соответствие",
}

ANSWER_TYPES = {
    ANSWER_TYPE_DELETE: "Удалено",
    ANSWER_TYPE_FREE: "Произвольный ответ",
    ANSWER_TYPE_CHOICE: "Выбор",
    ANSWER_TYPE_MATHEXP: "Математическое выражение",
    ANSWER_TYPE_MATHWRONG: "Математическое выражение с ошибками",
    ANSWER_TYPE_POINT: "Точка",
    ANSWER_TYPE_YESNO: "Да/нет",
    ANSWER_TYPE_INTERVAL: "Интервал",
    ANSWER_TYPE_INEQUALITY: "Неравенство",
    ANSWER_TYPE_EQUALITY: "Равенство",
    ANSWER_TYPE_CYRILLIC: "Текст (кириллица)",
    ANSWER_TYPE_MATCH: "Соответствие",
}

ANSWER_TYPES_DISPLAY = [(key, value) for key, value in ANSWER_TYPES.items()]

ANSWER_ERROR_RIGHT = 0
ANSWER_ERROR_NOT = 1
ANSWER_ERROR_CHOICE_LEN = 2
ANSWER_ERROR_CHOICE_SYM = 3
ANSWER_ERROR_MATH_SYM = 4
ANSWER_ERROR_MATH_CYR = 5
ANSWER_ERROR_MATH_PAR = 6
ANSWER_ERROR_MATH_PARSE = 7
ANSWER_ERROR_INEQ_UNDEF = 8
ANSWER_ERROR_EQ_UNDEF = 9
ANSWER_ERROR_EQ_PARSE = 10
ANSWER_ERROR_YESNO_NOT = 11
ANSWER_ERROR_MATHWRONG = 12
ANSWER_ERROR_NOINTER = 13
ANSWER_ERROR_WRONG_COUNT = 14

ANSWER_ERRORS = {
    ANSWER_ERROR_RIGHT: "Ответ правильный",
    ANSWER_ERROR_NOT: "Ответ корректный",
    ANSWER_ERROR_CHOICE_LEN: "Длина ответа должна быть равна одному символу",
    ANSWER_ERROR_CHOICE_SYM: "Неверный символ в ответе",
    ANSWER_ERROR_MATH_SYM: "В ответе присутствует недопустимый символ",
    ANSWER_ERROR_MATH_CYR: "Использование кириллицы недопустимо",
    ANSWER_ERROR_MATH_PAR: "Некорректная расстановка скобок",
    ANSWER_ERROR_MATH_PARSE: "Невозможно распарсить математическое выражение",
    ANSWER_ERROR_INEQ_UNDEF: "Неизвестная ошибка ввода интервала",
    ANSWER_ERROR_EQ_UNDEF: "Неизвестная ошибка ввода равенства",
    ANSWER_ERROR_EQ_PARSE: "Невозможно распарсить равенство",
    ANSWER_ERROR_YESNO_NOT: "Ответ не соответствует да/нет",
    ANSWER_ERROR_MATHWRONG: "Математическое выражение с ошибкой",
    ANSWER_ERROR_NOINTER: "Введенный ответ не соответствует интервалу или содержит недопустимые символы",
    ANSWER_ERROR_WRONG_COUNT: "Неверное количество ответов"
}

temp_nomath = re.compile(r'[^a-z0-9+±\-*/^=:|().,]+')
temp_math = re.compile(r'[a-z0-9+±=\-*/^:|().,]+')
temp_matherr = re.compile(r'[а-я0-9+±\-*/^=:|().,]+')
temp_ineq = re.compile(r'[a-z0-9+\-*/^=:|().,<>]+')
temp_equal = re.compile(r'[a-z0-9+\-*/^=:|().,]+')
temp_inter = re.compile(r'([(\[]+[^;]+;[^;]+[)\]]+)')


def is_interval(s):
    parts = list(map(lambda x: x[1:] if x[0] == ";" else x, temp_inter.findall(s)))
    if ';'.join(parts) == s:
        return parts
    else:
        return []


# app: study

MODULE_STATUS_IRRELEVANT = 'i'
MODULE_STATUS_LEARNING = 'l'
MODULE_STATUS_REPEATING = 'r'
MODULE_STATUS_DELETED = 'd'

MODULE_STATUSES = {
    MODULE_STATUS_IRRELEVANT: "Не актуально",
    MODULE_STATUS_LEARNING: "Изучение",
    MODULE_STATUS_REPEATING: "Закрепление",
    MODULE_STATUS_DELETED: "Удалено из программы"
}

MODULE_STATUSES_DISPLAY = list(MODULE_STATUSES.items())


MODULE_STATUS_ADD_REPEATING = 'ar'
MODULE_STATUS_ADD_LEARNING = 'al'
MODULE_STATUS_ADD_IRRELEVANT = 'ai'
MODULE_STATUS_DELETE_REPEATING = 'rd'
MODULE_STATUS_DELETE_LEARNING = 'ld'
MODULE_STATUS_DELETE_IRRELEVANT = 'id'
MODULE_STATUS_REPEATING_TO_LEARNING = 'rl'
MODULE_STATUS_REPEATING_TO_IRRELEVANT = 'ri'
MODULE_STATUS_LEARNING_TO_REPEATING = 'lr'
MODULE_STATUS_LEARNING_TO_IRRELEVANT = 'li'
MODULE_STATUS_IRRELEVANT_TO_LEARNING = 'il'
MODULE_STATUS_IRRELEVANT_TO_REPEATING = 'ir'


MODULE_STATUSES_SWITCH = {
    MODULE_STATUS_ADD_REPEATING: 'Добавить в "Повторение"',
    MODULE_STATUS_ADD_LEARNING: 'Добавить в "Изучение"',
    MODULE_STATUS_ADD_IRRELEVANT: 'Добавить в "Не актуально"',
    MODULE_STATUS_DELETE_REPEATING: 'Удалить из "Повторение"',
    MODULE_STATUS_DELETE_LEARNING: 'Удалить из "Изучение"',
    MODULE_STATUS_DELETE_IRRELEVANT: 'Удалить из "Не актуально"',
    MODULE_STATUS_REPEATING_TO_LEARNING: 'Переключить из "Повторение" в "Изучение"',
    MODULE_STATUS_REPEATING_TO_IRRELEVANT: 'Переключить из "Повторение" в "Не актуально"',
    MODULE_STATUS_LEARNING_TO_REPEATING: 'Переключить из "Изучение" в "Повторение"',
    MODULE_STATUS_LEARNING_TO_IRRELEVANT: 'Переключить из "Изучение" в "Не актуально"',
    MODULE_STATUS_IRRELEVANT_TO_LEARNING: 'Переключить из "Не актуально" в "Изучение"',
    MODULE_STATUS_IRRELEVANT_TO_REPEATING: 'Переключить из "Не актуально" в "Повторение"',
}

MODULE_STATUSES_SWITCH_DISPLAY = list(MODULE_STATUSES_SWITCH.items())


TEST_STATUS_CREATED = 'n'  # new
TEST_STATUS_OPENED = 'o'
TEST_STATUS_STARTED = 's'
TEST_STATUS_FINISHED = 'f'
TEST_STATUS_CLOSED = 'c'

TEST_STATUSES = {
    TEST_STATUS_CREATED: 'Создан',
    TEST_STATUS_OPENED: 'Открыт',
    TEST_STATUS_STARTED: 'Начат',
    TEST_STATUS_FINISHED: 'Выполнен',
    TEST_STATUS_CLOSED: 'Истек'
}

TEST_STATUSES_DISPLAY = list(TEST_STATUSES.items())

UNIT_STATUS_LEARNING = 'l'
UNIT_STATUS_REPEATING = 'r'

UNIT_STATUSES = {
    UNIT_STATUS_LEARNING: "Изучение",
    UNIT_STATUS_REPEATING: "Закрепление"
}

UNIT_STATUSES_DISPLAY = list(UNIT_STATUSES.items())

UNIT_COMPLETE_STATUS_NOTSTARTED = 'n'
UNIT_COMPLETE_STATUS_ACTIVE = 'a'
UNIT_COMPLETE_STATUS_FINISHED = 'f'

UNIT_COMPLETE_STATUSES = {
    UNIT_COMPLETE_STATUS_NOTSTARTED: "Не начат",
    UNIT_COMPLETE_STATUS_ACTIVE: "В процессе",
    UNIT_COMPLETE_STATUS_FINISHED: "Завершен"
}

UNIT_COMPLETE_STATUSES_DISPLAY = list(UNIT_COMPLETE_STATUSES.items())

ITEM_STATUS_NORESPONSE = 'n'
ITEM_STATUS_RIGHT = 'r'
ITEM_STATUS_CLEAR = 'c'
ITEM_STATUS_UNCLEAR = 'u'
ITEM_STATUS_DIFFICULT = 'd'
ITEM_STATUS_INCORRECT = 'i'
ITEM_STATUS_MODERATION = 'i'

ITEM_STATUSES = {
    ITEM_STATUS_NORESPONSE: "Ответ отсутствует",
    ITEM_STATUS_RIGHT: "Правильно",
    ITEM_STATUS_CLEAR: "Неправильно, понятно",
    ITEM_STATUS_UNCLEAR: "Неправильно, не понятно",
    ITEM_STATUS_DIFFICULT: "Затруднение с ответом",
    ITEM_STATUS_INCORRECT: "Некорректный ответ",
    ITEM_STATUS_MODERATION: "Отправлен на модерацию",
}

ITEM_STATUSES_DISPLAY = list(ITEM_STATUSES.items())

ITEM_ANALYSIS_NONE = 'n'
ITEM_ANALYSIS_TODO = 't'
ITEM_ANALYSIS_DONE = 'd'

ITEM_ANALYSISES = {
    ITEM_ANALYSIS_NONE: "Не требуется",
    ITEM_ANALYSIS_TODO: "В ожидании",
    ITEM_ANALYSIS_DONE: "Сделано"
}

ITEM_ANALYSISES_DISPLAY = list(ITEM_ANALYSISES.items())


FEATURES = ['A', 'AL', 'T', 'TL', 'P', 'D', 'R', 'E']
FEATURES_DOMAIN = ['A', 'T', 'L']


MODULE_COLOR_EMPTY = 'e'
MODULE_COLOR_PINK = 'p'
MODULE_COLOR_RED = 'r'
MODULE_COLOR_GREEN = 'g'

MODULE_COLORS = {
    MODULE_COLOR_GREEN: "#98FB98",
    MODULE_COLOR_RED: "#FFB6C1",
    MODULE_COLOR_PINK: "#fcebec",
    MODULE_COLOR_EMPTY: "#FFFFFF"
}

MODULE_COLORS_DISPLAY = list(MODULE_COLORS.items())


MULTIFEATURES = ['1', 'x0', 'x3', 'x8', 'x16', 'x24', 'x0^2', 'x0 x1', 'x0 x2', 'x0 x3', 'x0 x4', 'x0 x5', 'x0 x6',
                 'x0 x7', 'x0 x8', 'x0 x9', 'x0 x11', 'x0 x12', 'x0 x13', 'x0 x14', 'x0 x15', 'x0 x16', 'x0 x17',
                 'x0 x18', 'x0 x19', 'x0 x20', 'x0 x21', 'x0 x22', 'x0 x24', 'x0 x25', 'x0 x26', 'x0 x27', 'x0 x28',
                 'x0 x29', 'x0 x30', 'x0 x31', 'x0 x32', 'x0 x33', 'x0 x35', 'x1 x3', 'x1 x9', 'x1 x11', 'x1 x16',
                 'x1 x17', 'x1 x18', 'x1 x21', 'x1 x23', 'x1 x24', 'x1 x25', 'x1 x29', 'x1 x30', 'x1 x31', 'x1 x32',
                 'x1 x33', 'x2 x8', 'x2 x9', 'x2 x11', 'x2 x16', 'x2 x17', 'x2 x18', 'x2 x21', 'x2 x23', 'x2 x24',
                 'x2 x25', 'x2 x29', 'x2 x30', 'x2 x31', 'x2 x32', 'x2 x33', 'x3^2', 'x3 x4', 'x3 x5', 'x3 x6', 'x3 x7',
                 'x3 x8', 'x3 x9', 'x3 x11', 'x3 x13', 'x3 x16', 'x3 x17', 'x3 x19', 'x3 x21', 'x3 x23', 'x3 x24',
                 'x3 x25', 'x3 x30', 'x3 x31', 'x3 x32', 'x3 x33', 'x4 x10', 'x4 x16', 'x4 x17', 'x4 x24', 'x4 x25',
                 'x4 x32', 'x4 x33', 'x4 x34', 'x5 x10', 'x5 x11', 'x5 x16', 'x5 x17', 'x5 x24', 'x5 x25', 'x5 x32',
                 'x5 x33', 'x5 x34', 'x6 x10', 'x6 x11', 'x6 x16', 'x6 x17', 'x6 x24', 'x6 x25', 'x6 x32', 'x6 x33',
                 'x6 x34', 'x7 x11', 'x7 x16', 'x7 x17', 'x7 x25', 'x7 x33', 'x7 x34', 'x8^2', 'x8 x11', 'x8 x16',
                 'x8 x19', 'x8 x20', 'x8 x24', 'x8 x25', 'x9^2', 'x9 x11', 'x9 x19', 'x9 x20', 'x9 x21', 'x9 x22',
                 'x9 x23', 'x9 x25', 'x9 x27', 'x9 x29', 'x9 x31', 'x9 x35', 'x10 x23', 'x10 x24', 'x10 x27', 'x10 x31',
                 'x10 x35', 'x11 x13', 'x11 x14', 'x11 x15', 'x11 x16', 'x11 x17', 'x11 x18', 'x11 x25', 'x11 x26',
                 'x11 x31', 'x11 x32', 'x11 x33', 'x11 x34', 'x12 x19', 'x12 x25', 'x12 x33', 'x13 x19', 'x13 x21',
                 'x13 x25', 'x13 x29', 'x13 x33', 'x14 x25', 'x14 x33', 'x15^2', 'x15 x21', 'x15 x25', 'x15 x29',
                 'x15 x33', 'x16^2', 'x16 x19', 'x16 x24', 'x16 x25', 'x16 x28', 'x16 x29', 'x16 x32', 'x17^2',
                 'x17 x19', 'x17 x20', 'x17 x21', 'x17 x22', 'x17 x23', 'x17 x25', 'x17 x27', 'x17 x29', 'x17 x31',
                 'x17 x33', 'x17 x34', 'x18 x19', 'x18 x23', 'x18 x24', 'x18 x25', 'x18 x27', 'x18 x31', 'x18 x35',
                 'x19^2', 'x19 x23', 'x19 x24', 'x19 x25', 'x19 x26', 'x19 x29', 'x19 x31', 'x19 x32', 'x19 x33',
                 'x19 x34', 'x20 x25', 'x20 x32', 'x20 x33', 'x21 x26', 'x21 x29', 'x21 x32', 'x21 x33', 'x22 x33',
                 'x23^2', 'x23 x25', 'x23 x27', 'x23 x33', 'x23 x34', 'x24^2', 'x24 x27', 'x24 x32', 'x24 x33', 'x25^2',
                 'x25 x27', 'x25 x28', 'x25 x29', 'x25 x30', 'x25 x31', 'x25 x33', 'x26 x27', 'x26 x31', 'x26 x32',
                 'x27 x30', 'x27 x31', 'x27 x32', 'x27 x33', 'x27 x35', 'x29 x33', 'x31 x33', 'x31 x34', 'x31 x35',
                 'x32 x35', 'x33^2', 'x33 x35']



FILTER_HOMEWORK_WITH = '1'
FILTER_HOMEWORK_WITHOUT = '0'

FILTERS_HOMEWORK = [
    (FILTER_HOMEWORK_WITH, "С д/з на неделе"),
    (FILTER_HOMEWORK_WITHOUT, "Без д/з на неделе")
]

FILTER_ANALYSIS_WEEK = '2'
FILTER_ANALYSIS_MORE = '1'

FILTERS_ANALYSIS = [
    (FILTER_ANALYSIS_WEEK, "Не разобраны меньше недели"),
    (FILTER_ANALYSIS_MORE, "Не разобраны больше недели")
]

FILTER_REGRESS_REDPINK = 1
FILTER_REGRESS_PINK = 2
FILTER_REGRESS_RED = 3
FILTER_REGRESS_NO = 0

FILTERS_REGRESS = [
    (FILTER_REGRESS_REDPINK, "Есть регресс относительно последнего теста и среднего по теме"),
    (FILTER_REGRESS_PINK, "Есть регресс относительно последнего теста"),
    (FILTER_REGRESS_RED, "Есть регресс относительно среднего по теме"),
    (FILTER_REGRESS_NO, "Нет явного регресса")
]

FILTER_LEARNING_EMPTY = 0
FILTER_LEARNING_HAS_NOT = 1
FILTER_LEARNING_HAS = 2

FILTERS_LEARNING = [
    (FILTER_LEARNING_HAS_NOT, "Нет трудностей"),
    (FILTER_LEARNING_HAS, "Есть трудности")
]

FILTER_TESTTASK_ANALYSIS_NO = 0
FILTER_TESTTASK_ANALYSIS_YES = 1

FILTERS_TESTTASK_ANALYSIS = [
    (FILTER_TESTTASK_ANALYSIS_YES, "Разобранные задания"),
    (FILTER_TESTTASK_ANALYSIS_NO, "Нужно разобрать")
]
