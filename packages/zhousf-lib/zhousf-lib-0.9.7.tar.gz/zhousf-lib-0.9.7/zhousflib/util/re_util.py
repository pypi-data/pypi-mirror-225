# -*- coding: utf-8 -*-
# @Author  : zhousf
# @Function:
import re


def get_digit_char(string: str):
    # 提取数字
    return re.sub(u"([^\u0030-\u0039])", "", string)


def only_contain_letter_char(self, string: str):
    """
    仅包含字母
    """
    return len(self.get_letter_char(string)) == len(string)


def get_letter_char(string: str):
    # 提取大小写字母
    return re.sub(u"([^\u0041-\u005a\u0061-\u007a])", "", string)


def get_digit_letter_char(string: str):
    # 提取大小写字母、数字
    return re.sub(u"([^\u0041-\u005a\u0061-\u007a\u0030-\u0039])", "", string)