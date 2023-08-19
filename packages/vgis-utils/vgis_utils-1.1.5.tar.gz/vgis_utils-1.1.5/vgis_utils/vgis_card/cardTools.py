"""
#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
@Project :pythonCodeSnippet
@File    :cardTools.py
@IDE     :PyCharm
@Author  :chenxw
@Date    :2023/8/17 11:28
@Descr:  证件信息判断和提取
"""
import re


class CardHelper:
    def __init__(self):
        pass

    # 验证身份证号是否有效
    @staticmethod
    def is_valid_of_identity_card(identity_card):
        is_valid = False
        # pattern = r'^[1-9]d{5}[1-9]d{3}(0[1-9]|1[0-2])(0[1-9]|[1-2]d|3[0-1])d{3}[dX]$'
        pattern = r'^[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|(3[0-1]))\d{3}[\dXx]$'
        if re.match(pattern, identity_card):
            is_valid = True
        else:
            is_valid = False
        return is_valid

    # 通过身份证号获取性别
    @staticmethod
    def get_sex_by_identity_card(identity_card):

        sex = identity_card[16:17]
        if int(sex) % 2:
            sex = '男'
        else:
            sex = '女'
        return sex

    # 通过身份证号获取出生日期
    @staticmethod
    def get_birthday_by_identity_card(identity_card):

        year = identity_card[6:10]
        month = identity_card[10:12]
        date = identity_card[12:14]
        birthy = year + '-' + month + '-' + date
        return birthy
