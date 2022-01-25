import re

from sympy import solve, Eq, simplify
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application

import const

transformations = (standard_transformations + (implicit_multiplication_application,))


class AnswerBase:
    text = ''

    def __init__(self, text):
        self.text = text

    def __str__(self):
        return "Answer: " + self.text

    def syntax_check(self, student_answer):
        pass

    def semantic_check(self, student_answer):
        pass


class AnswerChoice(AnswerBase):

    def get_type(self):
        return const.ANSWER_TYPE_CHOICE

    def syntax_check(self, student_answer):
        ans = ''.join(student_answer.split()).lower()
        if len(ans) != 1:
            return const.ANSWER_ERROR_CHOICE_LEN
        elif re.match(r'[1-6а-еa-f]', ans) is None:
            return const.ANSWER_ERROR_CHOICE_SYM
        else:
            return const.ANSWER_ERROR_NOT

    def semantic_check(self, student_answer):
        ans = ''.join(student_answer.split()).lower()
        correct = 'abcdef123456абвгде'
        if ((correct.find(ans) % 6) == (correct.find(self.text) % 6)) and self.syntax_check(
                ans) == const.ANSWER_ERROR_NOT:
            return const.ANSWER_ERROR_RIGHT
        else:
            return self.syntax_check(ans)


class AnswerMathExp(AnswerBase):

    def get_type(self):
        return const.ANSWER_TYPE_MATHEXP

    def syntax_check(self, student_answer):
        ans = ''.join(student_answer.split()).lower()
        ans = ans.replace("^", "**")
        ans = ans.replace(":", "/")
        ans = ans.replace("|", "+")
        if re.search(r'[а-яА-Я]+', ans) is not None:
            return const.ANSWER_ERROR_MATH_CYR
        if const.temp_nomath.search(ans) is not None:
            return const.ANSWER_ERROR_MATH_SYM
        elif not const.par_checker(ans):
            return const.ANSWER_ERROR_MATH_PAR
        else:
            try:
                parse_expr(ans, transformations=transformations)
                return const.ANSWER_ERROR_NOT
            except Exception:
                return const.ANSWER_ERROR_MATH_PARSE

    def semantic_check(self, student_answer):
        ans = ''.join(student_answer.split()).lower()
        ans = ans.replace("^", "**").replace(":", "/").replace("|", "+")
        cor_ans = self.text.replace("^", "**").replace(":", "/").replace("|", "+")
        try:
            math_stu = parse_expr(ans, transformations=transformations)
            math_cor = parse_expr(cor_ans, transformations=transformations)
            if simplify(math_stu - math_cor) == 0 and self.syntax_check(ans) == const.ANSWER_ERROR_NOT:
                return const.ANSWER_ERROR_RIGHT
            else:
                return self.syntax_check(ans)
        except Exception:
            return self.syntax_check(ans)


class AnswerPoint(AnswerBase):

    def get_type(self):
        return const.ANSWER_TYPE_POINT

    def syntax_check(self, student_answer):
        ans = ''.join(student_answer.split()).lower()
        if const.is_interval(ans):
            return const.ANSWER_ERROR_NOT

    def semantic_check(self, student_answer):
        ans = ''.join(student_answer.split()).lower()
        if self.text == ans and self.syntax_check(ans) == const.ANSWER_ERROR_NOT:
            return const.ANSWER_ERROR_RIGHT
        else:
            return self.syntax_check(ans)


class AnswerMathWrong(AnswerBase):

    def get_type(self):
        return const.ANSWER_TYPE_POINT

    def syntax_check(self, student_answer):
        return const.ANSWER_ERROR_MATHWRONG

    def semantic_check(self, student_answer):
        return const.ANSWER_ERROR_MATHWRONG


class AnswerInterval(AnswerBase):

    def get_type(self):
        return const.ANSWER_TYPE_INTERVAL

    def syntax_check(self, student_answer):
        ans = ''.join(student_answer.split()).lower()
        if bool(const.is_interval(ans)):
            return const.ANSWER_ERROR_NOT
        else:
            return const.ANSWER_ERROR_NOINTER

    def semantic_check(self, student_answer):
        ans = ''.join(student_answer.split()).lower()
        if ans == self.text and self.syntax_check(ans) == const.ANSWER_ERROR_NOT:
            return const.ANSWER_ERROR_RIGHT
        else:
            return self.syntax_check(ans)


class AnswerInequality(AnswerBase):

    def get_type(self):
        return const.ANSWER_TYPE_INEQUALITY

    def syntax_check(self, student_answer):
        ans = ''.join(student_answer.split()).lower()
        if (re.search(r'[<>]', ans) is not None or re.search(r'/=', ans) is not None) and const.temp_ineq.match(
                ans) is not None:
            return const.ANSWER_ERROR_NOT
        else:
            return const.ANSWER_ERROR_INEQ_UNDEF

    def semantic_check(self, student_answer):
        ans = ''.join(student_answer.split()).lower()
        if self.text == ans and self.syntax_check(ans) == const.ANSWER_ERROR_NOT:
            return const.ANSWER_ERROR_RIGHT
        else:
            return self.syntax_check(ans)


class AnswerEquality(AnswerBase):

    def get_type(self):
        return const.ANSWER_TYPE_EQUALITY

    def syntax_check(self, student_answer):
        ans = ''.join(student_answer.split()).lower()
        ans = ans.replace("^", "**")
        ans = ans.replace(":", "/")
        if const.temp_math.match(ans) is not None and "=" in ans:
            try:
                exprs = ans.split("=")
                math_exprs = []
                for expr in exprs:
                    math_exprs.append(parse_expr(expr, transformations=transformations))
                return const.ANSWER_ERROR_NOT
            except Exception:
                return const.ANSWER_ERROR_EQ_PARSE
        else:
            return const.ANSWER_ERROR_EQ_UNDEF

    def semantic_check(self, student_answer):
        ans = ''.join(student_answer.split()).lower()
        ans = ans.replace("^", "**")
        ans = ans.replace(":", "/")
        try:
            left_stu, right_stu = [parse_expr(expr, transformations=transformations) for expr in ans.split("=")]
            left_cor, right_cor = [parse_expr(expr, transformations=transformations) for expr in self.text.split("=")]
            if solve(Eq(left_stu, right_stu)) == solve(Eq(left_cor, right_cor)) and self.syntax_check(
                    ans) == const.ANSWER_ERROR_NOT:
                return const.ANSWER_ERROR_RIGHT
            else:
                return self.syntax_check(ans)
        except Exception:
            return self.syntax_check(ans)


class AnswerYesno(AnswerBase):

    def get_type(self):
        return const.ANSWER_TYPE_YESNO

    def syntax_check(self, student_answer):
        ans = ''.join(student_answer.split()).lower()
        if ans in ['да', 'нет']:
            return const.ANSWER_ERROR_NOT
        else:
            return const.ANSWER_ERROR_YESNO_NOT

    def semantic_check(self, student_answer):
        ans = ''.join(student_answer.split()).lower()
        if self.text == ans and self.syntax_check(ans) == const.ANSWER_ERROR_NOT:
            return const.ANSWER_ERROR_RIGHT
        else:
            return self.syntax_check(ans)


class AnswerMatch(AnswerBase):

    def get_type(self):
        return const.ANSWER_TYPE_MATCH

    def syntax_check(self, student_answer):
        return const.ANSWER_ERROR_NOT

    def semantic_check(self, student_answer):
        ans = ''.join(student_answer.split()).lower()
        if self.text == ans and self.syntax_check(ans) == const.ANSWER_ERROR_NOT:
            return const.ANSWER_ERROR_RIGHT
        else:
            return self.syntax_check(ans)


class AnswerFree(AnswerBase):

    def get_type(self):
        return const.ANSWER_TYPE_FREE

    def syntax_check(self, student_answer):
        return const.ANSWER_ERROR_NOT

    def semantic_check(self, student_answer):
        ans = ''.join(student_answer.split()).lower()
        if self.text == ans and self.syntax_check(ans) == const.ANSWER_ERROR_NOT:
            return const.ANSWER_ERROR_RIGHT
        else:
            return self.syntax_check(ans)


class AnswerCyrillic(AnswerBase):

    def get_type(self):
        return const.ANSWER_TYPE_CYRILLIC

    def syntax_check(self, student_answer):
        return const.ANSWER_ERROR_NOT

    def semantic_check(self, student_answer):
        ans = ''.join(student_answer.split()).lower()
        if self.text == ans and self.syntax_check(ans) == const.ANSWER_ERROR_NOT:
            return const.ANSWER_ERROR_RIGHT
        else:
            return self.syntax_check(ans)


ANSWER_CLASSES = {
    const.ANSWER_TYPE_FREE: AnswerFree,
    const.ANSWER_TYPE_CHOICE: AnswerChoice,
    const.ANSWER_TYPE_MATHEXP: AnswerMathExp,
    const.ANSWER_TYPE_MATHWRONG: AnswerMathWrong,
    const.ANSWER_TYPE_POINT: AnswerPoint,
    const.ANSWER_TYPE_YESNO: AnswerYesno,
    const.ANSWER_TYPE_INTERVAL: AnswerInterval,
    const.ANSWER_TYPE_INEQUALITY: AnswerInequality,
    const.ANSWER_TYPE_EQUALITY: AnswerEquality,
    const.ANSWER_TYPE_CYRILLIC: AnswerCyrillic,
    const.ANSWER_TYPE_MATCH: AnswerMatch,
}
