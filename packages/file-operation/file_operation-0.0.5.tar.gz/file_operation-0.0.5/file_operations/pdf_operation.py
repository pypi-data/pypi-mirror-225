# -*- coding: utf-8 -*-
"""
@Time : 2023/8/16 21:13 
@Author : skyoceanchen
@TEL: 18916403796
@项目：文件使用
@File : pdf_operation.by
@PRODUCT_NAME :PyCharm
"""
import pdfplumber  # pip install pdfplumber


class PdfOperation(object):
    def __init__(self, path):
        self.path = path

    def read_pdf(self):
        pdf = pdfplumber.open(self.path)
        text_list = []
        # 解析pdf全部内容
        for i in pdf.pages:
            text = i.extract_text().replace("\u3000", "").replace("\xa0", "").replace("—", "").replace("(cid:122)", '')
            # str1 += i.extract_text().replace('', '')
            text_list.append(text)
        text = ''.join(text_list)
        return text
