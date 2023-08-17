# -*- coding: utf-8 -*-
"""
@Time : 2023/8/11 18:29 
@Author : skyoceanchen
@TEL: 18916403796
@项目：file_operations
@File : configparser_operation.by
@PRODUCT_NAME :PyCharm
"""
# media/test.cfg
import configparser


class ConfigParser(object):
    def __init__(self, path):
        self.path = path
        # 创建一个解析器
        self.config = configparser.ConfigParser()
        # 读取并解析test.cfg
        self.config.read('test.cfg', encoding='utf-8')

    def read(self):
        pass

    # 获取分区
    def sections(self):
        return self.config.sections()

    # 获取选项
    def options(self, section):
        return self.config.options(section)

    # 获取某个选项的值
    def option_value(self, section, option, data_type=None):
        """
        :param section:
        :param option:
        :param data_type:int float db
        :return:
        """
        if data_type == "int":
            return self.config.getint(section, option)
        elif data_type == "float":
            return self.config.getfloat(section, option)
        elif data_type == "bool":
            return self.config.getboolean(section, option)
        else:
            return self.config.get(section, option)

    # 是否有某个分区
    def has_section(self, section):
        return self.config.has_section(section)

    # 是否有某个选项
    def has_option(self, section, option):
        self.config.has_option(section, option)

    # # 添加分区
    def add_section(self, section):
        self.config.add_section(section)

    # # 删除选项
    def remove_option(self, section, option):
        self.config.remove_option(section, option)

    #  添加/  修改
    def set_option(self, section, option, value):
        self.config.set(section, option, value)

    # # 增删改查操作完成后写回文件中
    def save(self):
        with open(self.path, "wt", encoding="utf-8") as f:
            self.config.write(f)
