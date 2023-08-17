# -*- coding:utf-8 -*-
"""
@Time : 2023/3/22
@Author : skyoceanchen
@TEL: 18916403796
@File : other_operation.py 
@PRODUCT_NAME : PyCharm 
"""


class ReadDat(object):
    def read_dat(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        return text
