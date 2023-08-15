"""
===================================
#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
@Author: chenxw
@Email : gisfanmachel@gmail.com
@File: excelTools.py
@Date: Create in 2021/1/28 11:53
@Description: excel操作类
@ Software: PyCharm
===================================
"""
import os
import string

import pandas as pd

from vgis_utils.vgis_list.listTools import ListHelper


class ExcelHelper:

    # 判断excel表里是否有某列
    @staticmethod
    def is_has_field_in_excel(excel_obj, field_name):
        is_find = False
        column_list = excel_obj.columns.values
        for field_index in range(len(column_list)):
            if column_list[field_index].strip() == field_name.strip():
                is_find = True
                break
        return is_find
    @staticmethod
    # 通过excel字段名获取字段索引，若没找到，则为-1
    def get_field_index_by_name_in_excel(excel_obj, field_name):
        field_index_need = -1
        column_list = excel_obj.columns.values
        for field_index in range(len(column_list)):
            if column_list[field_index].strip() == field_name.strip():
                field_index_need = field_index
                break
        return field_index_need

    @staticmethod
    # 通过excel字段名和行号获取字段值
    def get_field_value_by_name_in_excel(excel_obj, row_index, field_name):
        field_index_need = -1
        column_list = excel_obj.columns.values
        for field_index in range(len(column_list)):
            if column_list[field_index].strip() == field_name.strip():
                field_index_need = field_index
                break
        row_values = excel_obj.values[row_index]
        return row_values[field_index_need]

    @staticmethod
    # 获取excel的字段个数
    def get_field_count_in_excel(excel_obj):
        column_list = excel_obj.columns.values
        return len(column_list)

    @staticmethod
    # 为excel增加一列
    def add_field_in_excel(excel_obj, field_name):
        excel_obj[field_name] = None

    @staticmethod
    # 读取excel表内容指定行数据
    def read_excel_data_values_by_row(excel_obj, row_num):
        for row_index in range(len(excel_obj)):
            # excel内容从第二行开始
            if row_index == row_num - 1:
                result_row_values = excel_obj.values[row_index]
                return result_row_values

    @staticmethod
    #  读取excel表字段
    def read_excel_data_columns(excel_obj):
        result_row_values = excel_obj.columns
        return result_row_values

    @staticmethod
    # 构建excel结果数据
    def build_data_excel(result_excel_path, all_data_list):
        file_dir_exists = os.path.exists(os.path.dirname(result_excel_path))
        if file_dir_exists is False:
            os.makedirs(os.path.dirname(result_excel_path))
        if os.path.exists(result_excel_path):
            os.remove(result_excel_path)
        if len(all_data_list) > 0:
            with pd.ExcelWriter(result_excel_path) as writer:
                for i in range(len(all_data_list)):
                    each_data_list = all_data_list[i]
                    if len(each_data_list) > 1:
                        df = pd.DataFrame(each_data_list,
                                          columns=ListHelper.get_key_name_str(each_data_list[0]))
                        sheet_name_str = "sheet" + str(i + 1)
                        df.to_excel(writer, sheet_name=sheet_name_str, index=False, startrow=0, encoding="utf_8_sig")
                # writer.save()
                # writer.close()
        else:
            # 创建空白excel
            fd = open(result_excel_path, 'w')
            fd.close()




    @staticmethod
    # 根据Excel列索引值生成列字母名
    def get_column_name(column_index):
        ret = ''
        ci = column_index - 1
        index = ci // 26
        if index > 0:
            ret += ExcelHelper.get_column_name(index)
        ret += string.ascii_uppercase[ci % 26]
        return ret