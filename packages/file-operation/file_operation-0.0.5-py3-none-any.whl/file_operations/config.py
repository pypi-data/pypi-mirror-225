# -*- coding: utf-8 -*-
"""
@Time : 2023/8/10 14:24 
@Author : skyoceanchen
@TEL: 18916403796
@项目：文件使用
@File : config.by
@PRODUCT_NAME :PyCharm
"""
import os

DIRNAME = os.path.dirname(os.path.abspath(__file__))
WKHMLTOPDF = os.path.join(DIRNAME, "media", "wkhtmltox", 'wkhtmltopdf.exe')
PANDOC = os.path.join(DIRNAME,"media", "Pandoc", 'pandoc.exe')
