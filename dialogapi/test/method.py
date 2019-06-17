import re


class AssertionMethodFactory:
    def __init__(self):
        clses = [AssertEqual, AssertIn, AssertRegexEqual, AssertRegexIn,
                 AssertNotEqual, AssertNotIn, AssertRegexNotEqual,
                 AssertRegexNotIn,
                 ]
        self._mapper = {mt.name: mt for mt in clses}

    def build(self, method_name):
        """
        Args:
            method (str): テスト関数の名前
        """
        return self._mapper[method_name]()


class AssertEqual:
    name = "equal"

    def execute(self, first, second):
        return first == second


class AssertIn:
    name = "in"

    def execute(self, first, second):
        return first in second


class AssertRegexEqual:
    name = "regex_equal"

    def execute(self, first, second):
        match = re.search(second, first)
        return bool(match)


class AssertRegexIn:
    name = "regex_in"

    def execute(self, first, second):
        for regex in second:
            if bool(re.search(regex, first)):
                return True
        return False


class AssertNotEqual:
    name = "not_equal"

    def execute(self, first, second):
        return first != second


class AssertNotIn:
    name = "not_in"

    def execute(self, first, second):
        return first not in second


class AssertRegexNotEqual:
    name = "regex_not_equal"

    def execute(self, first, second):
        match = re.search(second, first)
        return not bool(match)


class AssertRegexNotIn:
    name = "regex_not_in"

    def execute(self, first, second):
        for regex in second:
            if bool(re.search(regex, first)):
                return False
        return True
