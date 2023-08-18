#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
# @Time    :  2023/6/27 14:20
# @Author  : chenxw
# @Email   : gisfanmachel@gmail.com
# @File    : listTools.py
# @Descr   : 
# @Software: PyCharm
from operator import itemgetter


class ListHelper:
    def __int__(self):
        pass



    @staticmethod
    # 数组去重
    def remove_same_item(ids):
        news_ids = []
        for id in ids:
            if id not in news_ids:
                news_ids.append(id)
        return news_ids

    @staticmethod
    # 去掉数组中重复项
    def remove_same_element_of_list(ele_list):
        new_ele_list = []
        for ele in ele_list:
            if ele not in new_ele_list:
                new_ele_list.append(ele)
        return new_ele_list

    @staticmethod
    # 去掉数组中空白项
    def remove_blank_elment_of_list(ele_list):
        new_ele_list = []
        for ele in ele_list:
            if str(str(ele).strip()) != "":
                new_ele_list.append(ele)
        return new_ele_list

    @staticmethod
    # 查找元素在数组中的索引号
    def get_index_in_list_of_elment(element, ele_list):
        # index = ele_list.index(element)
        return_index = -1
        for index in range(len(ele_list)):
            if ele_list[index] == element:
                return_index = index
                break
        return return_index

    @staticmethod
    # 获取项目在数组中出现的次数
    def get_value_count_in_list(value, value_list):
        count = 0
        for tempvalue in value_list:
            if value == tempvalue:
                count = count + 1
        return count

    @staticmethod
    # 获取dict里包含的字段列
    def get_key_name_str(data_dict):
        columns = []
        for key, value in data_dict.items():
            columns.append(key)
        return columns


    @staticmethod
    # 删除对象里不要的key
    def remove_keys_in_obj(obj, remove_key_list):
        for remove_key in remove_key_list:
            if remove_key in obj:
                del obj[remove_key]


    @staticmethod
    # 将所有数组合并成一个数组
    def convert_all_list_into_one_list( all_data_record_list):
        result_data_list = []
        for each_data_record_list in all_data_record_list:
            for data_field_value_obj in each_data_record_list:
                result_data_list.append(data_field_value_obj)
        return result_data_list

    @staticmethod
    def get_number_str_by_list(num_list):
        number_str = ""
        for num in num_list:
            number_str = number_str + str(num) + ","
        number_str = number_str.rstrip(",")
        return number_str

    @staticmethod
    # 对dict里的字典内容进行排序
    def sort_dict_by_filed(item_list, sort_field):
        return sorted(item_list, key=itemgetter(sort_field))

    @staticmethod
    # 判断dict字典是否有搜索对象
    def is_has_item_in_dict(search_item_value, item_list):
        is_find = False
        for item_name in item_list:
            if item_name == search_item_value:
                is_find = True
                break
        return is_find

