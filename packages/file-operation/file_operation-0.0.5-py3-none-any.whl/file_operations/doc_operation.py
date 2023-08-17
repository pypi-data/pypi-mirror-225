# -*- coding: utf-8 -*-
"""
@Time : 2023/8/16 21:11 
@Author : skyoceanchen
@TEL: 18916403796
@项目：文件使用
@File : doc_operation.by
@PRODUCT_NAME :PyCharm
"""

# from win32com import client as wc  # pip install pywin32
from win32com.client import Dispatch


class DocOperation(object):
    def __init__(self, path):
        self.path = path

    def read_doc(self):
        word = Dispatch('Word.Application')  # 打开word应用程序
        word.Visible = 0  # 后台运行,不显示
        word.DisplayAlerts = 0  # 不警告
        doc = word.Documents.Open(FileName=self.path, Encoding='gbk')
        text_list = []
        for para in doc.paragraphs:
            text = para.Range.Text.replace("\x15", "").replace("\x01", "").replace("\x0c", "").replace("\x07",
                                                                                                       "").replace(
                "\r", "").replace("\x0e", "")
            # text = ''.join(para.Range.Text.strip(" ").split('\r'))
            if text:
                text_list.append(text)
        doc.Close()
        word.Quit()
        text = "".join(text_list)
        return text
