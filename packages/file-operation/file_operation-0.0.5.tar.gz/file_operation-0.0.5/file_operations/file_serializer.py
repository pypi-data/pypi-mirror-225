# -*- coding: utf-8 -*-
"""
@Time : 2023/8/11 17:28
@Author : skyoceanchen
@TEL: 18916403796
@项目：file_operations
@File : pickle_operation.by
@PRODUCT_NAME :PyCharm
"""

import pickle  # ，还有跟python2它完全一样的叫做 cpickle，两者的区别就是后者更快。所以，下面操作
# 中，不管是用import pickle ，还是用import cpickle as pickle ，在功能上都是一样的
import os


class PickleOperation(object):
    def __init__(self, path):
        self.path = path

    def write(self, data):
        """
        :param data: { "a":[1, 2, 3, 4, 5]}
        :return:
        """
        f = open(self.path, "wb")
        # pickle.dump(data, f)  ##文件中以 ascii 格式保存数据
        # 二进制存储文件更小
        pickle.dump(data, f, True)  ##文件中以二进制格式保存数据
        f.close()

    def read(self):
        return pickle.load(open(self.path, "rb"))

    def st_size(self, path1, path2):
        s1 = os.stat(path1).st_size
        s2 = os.stat(path2).st_size
        return s1, s2


import shelve

"""
利用shelve 模块，你可以将Python 程序中的变量保存到二进制的shelf 文件中。
这样，程序就可以从硬盘中恢复变量的数据。shelve 模块让你在程序中添加“保存”
和“打开”功能。例如，如果运行一个程序，并输入了一些配置设置，就可以将这
些设置保存到一个shelf 文件，然后让程序下一次运行时加载它们。
"""
"""
在Windows 上运行前面的代码，你会看到在当前工作目录下有3 个新文件：
mydata.bak、mydata.dat 和mydata.dir。在OS X 上，只会创建一个mydata.db 文件。
"""
"""
shelf 值不必用读模式或写模式打开，因为它们在打开后，既能读又能写
"""


class ShelveOperation(object):
    def __init__(self, path_name):
        self.path_name = path_name
        self.shelve_file = shelve.open(self.path_name)

    def write(self, data):
        self.shelve_file['key'] = data
        self.close()

    def read(self):
        data = self.shelve_file['key']
        self.close()
        return data

    def close(self):
        self.shelve_file.close()

    # 编码
    def keyencoding(self):
        return self.shelve_file.keyencoding
