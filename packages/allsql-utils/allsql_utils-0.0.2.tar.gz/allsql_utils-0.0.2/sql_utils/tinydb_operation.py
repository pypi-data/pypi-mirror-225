# -*- coding:utf-8 -*-
"""
@Time : 2022/10/29
@Author : skyoceanchen

@TEL: 18916403796
@File : tinydb_operation.py 
@PRODUCT_NAME : PyCharm 
"""
from tinydb import TinyDB  # '4.7.0'
from tinydb import Query

q = Query()
db = TinyDB('db.json')
db.insert({'type': 'apple', 'count': 7})
db.insert({'type': 'peach', 'count': 3})
db.update({'type': 'bar111'}, q.id == "bar")
print(db.all())
