# -*- coding: utf-8 -*-
"""
@Time : 2023/8/16 21:09 
@Author : skyoceanchen
@TEL: 18916403796
@项目：文件使用
@File : docx_operation.by
@PRODUCT_NAME :PyCharm
"""
import docx  # pip install python-docx


class DocxOperation(object):
    def __init__(self, path):
        self.path = path

    def read_docx(self):
        doc = docx.Document(self.path)  # 绝对路径
        # 读取表格外全部内容
        text_list = []
        for i in doc.paragraphs:
            text = i.text.replace("—", "")
            if text:
                text_list.append(text)
        text = ''.join(text_list)
        return text
