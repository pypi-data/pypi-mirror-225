#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:skyoceanchen
# project_name:myself_exercise
# py_name :保存excel
# software: PyCharm
# datetime:2021/6/26 15:27
import xlwt


# <editor-fold desc="保存excel--xlwt-xls">
class SaveExcelDateXLS(object):
    def __init__(self, file_name=None):
        """
        :param file_name:文件名称
        :param sheet_name: 表名
        :param header_list: 表头
        :param content_list: 内容 二进制
        """
        self.file_name = file_name
        # # 创建一个workbook 设置编码
        # workbook = xlwt.Workbook(encoding = 'utf-8')
        self.book = xlwt.Workbook(
            encoding='utf-8',
            # encoding='ascii',
            # style_compression=0
        )

    def add_sheet(self, sheet_name=None):
        self.sheet = self.book.add_sheet(sheet_name, cell_overwrite_ok=True)

    def header_table(self, header_list):
        for index, header in enumerate(header_list):
            self.sheet.write(0, index, header)

    def content(self, content_list):
        rows = len(content_list)
        # cols = len(content_list[0])
        old_rows = len(self.sheet.rows)
        for i in range(rows):
            for j in range(len(content_list[i])):
                self.sheet.write(i + old_rows, j, content_list[i][j])
        # print(111111111, self.sheet.rows,len(self.sheet.rows))
        # print(22222222222, self.sheet.col)

    def save(self):
        self.book.save(self.file_name)
# xls = SaveExcelDateXLS(file_name="1.xls")
# xls.add_sheet('wokk')
# xls.header_table([1, 2, 3, 4, 5])
# xls.header_table([1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
# xls.header_table([3, 4, 52, 3, 4, 5])
# xls.content([[1, 2, 3, 4, 5], [5, 3, 2, "发射点发射点发射点发合法的手续和", 2], [4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 1, 2, 3]])
# xls.content([[1, 2, 3, 44, 5, 566, 76, 7, 1, 88, 8, 89, 9, 9, 1, 2, 3, 4, 5], [5, 3, 2, 1, 2],
#              [4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 1, 2, 3]])
#
# xls.save()
# </editor-fold>
