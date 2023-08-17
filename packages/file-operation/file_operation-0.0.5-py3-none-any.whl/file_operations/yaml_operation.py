# -*- coding: utf-8 -*-
"""
@Time : 2023/8/10 16:24 
@Author : skyoceanchen
@TEL: 18916403796
@项目：文件使用
@File : yaml_operations.by
@PRODUCT_NAME :PyCharm
"""
import yaml  # pyyaml-6.0.1

"""
print(yaml.dump({'name': 'iswbm', 'age': 18, 'gender': 'male'}))
# '!munch.Munch\nbar: 100\nfoo: !munch.Munch\n  lol: true\nmsg: hello\n'
# print(yaml.dump(munch_obj))
# '''!munch.Munch
# bar: 100
# foo: !munch.Munch
#   lol: true
# msg: hello'''
#
# # 建议使用 safe_dump 去掉 !munch.Munch
# '''bar: 100
# foo:
#   lol: true
# msg: hello'''
file = open('yaml_file.yaml', 'w', encoding='utf-8')
yaml.dump({'name':{ 'iswbm':"111"}, 'age': 18, 'gender': 'male'}, file)
file.close()



"""
