#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Email : 807447312@qq.com
@Time  : 2023/1/13 23:47
@File  : ExcelUtils.py
'''

import xlrd

def read_excel(file_path):
    workbook = xlrd.open_workbook(file_path)
    sheet = workbook.sheet_by_index(0)  # 假设用例在第一个sheet中

    # 获取标题列、操作数据列和预期结果列的索引
    title_col_index = None
    data_col_index = None
    expected_result_col_index = None

    for col_index in range(sheet.ncols):
        cell_value = sheet.cell_value(0, col_index)
        if cell_value == "标题列":
            title_col_index = col_index
        elif cell_value == "操作数据列":
            data_col_index = col_index
        elif cell_value == "预期结果列":
            expected_result_col_index = col_index

    if title_col_index is None or data_col_index is None or expected_result_col_index is None:
        raise ValueError("未找到标题列、操作数据列或预期结果列")

    # 读取用例数据
    test_cases = []
    for row_index in range(1, sheet.nrows):
        title = sheet.cell_value(row_index, title_col_index)
        data = sheet.cell_value(row_index, data_col_index)
        expected_result = sheet.cell_value(row_index, expected_result_col_index)
        test_cases.append((title, data, expected_result))

    return test_cases
