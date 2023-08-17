# -*- coding:utf-8 -*-
"""
@Time : 2023/3/25
@Author : skyoceanchen

@TEL: 18916403796
@File : mdb_operation.py 
@PRODUCT_NAME : PyCharm 
"""

import pyodbc  # pyodbc-4.0.39


class MDBOperation(object):
    def __init__(self, path):
        # p_path = r'E:\Programs\FBG86002-客户端2.9.2带时间戳\客户端带时间戳\历史记录\报警记录.mdb'
        self.path = path
        self.driver = '{Microsoft Access Driver (*.mdb, *.accdb)}'
        # 'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + p_path + ';PWD=007'
        self.conn = pyodbc.connect(f'Driver={self.driver};DBQ={self.path}')
        self.cur = self.conn.cursor()

    # 查看当前数据库中所有的表
    def show_tables(self):
        tables = []
        for table_name in self.cur.tables(tableType='TABLE'):
            tables.append(table_name.table_name)
        return tables

    # <editor-fold desc="查询数据">
    def select(self, sql):
        """
        :param     sql = "SELECT * FROM " + f'{table}'  # 取表 ActualValues_T
        :return:
        """
        self.cur.execute(sql)
        results = self.cur.fetchall()  # 取 ActualValues_T 所有数据
        return list(results)

    # 关闭数据库
    def close(self):
        self.conn.close()
