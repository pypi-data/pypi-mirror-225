#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:skyoceanchen
# project_name:automaticoffice
# py_name :acx-21
# software: PyCharm
# datetime:2021/8/6 9:39


import pymssql  # 引入pymssql模块  pip  installed pymssql==2.2.8


class SQLServer(object):
    def __init__(self, host='39.108.174.172:8081', user='sa', password='@Pursun2018.', database='JHWData',
                 charset='cp936', write_log=None,
                 # charset='GB2312',
                 # charset='utf-8',
                 # charset='gbk',
                 autocommit=True):
        try:
            self.conn = pymssql.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                charset=charset
            )  # 服务器名,账户,密码,数据库名
            self.write_log = write_log
            if self.conn:
                write_log.write_log_to_Text('连接数据库成功，可以插入....', 'blue')
            self.cursor = self.conn.cursor(
                as_dict=True
            )
        except:
            self.write_log.write_log_to_Text('连接数据库失败，程序崩溃，请联系开发者....', 'blue')

    # <editor-fold desc="查看所有的表">
    def show_table(self, sql=None):
        sql = "select name from sysobjects where xtype='u'"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    # </editor-fold>
    # <editor-fold desc="查询表的所有字段">
    def show_table_field(self, sql=None):
        sql = """select name from syscolumns where id=(select max(id) from sysobjects where xtype='u' and name='OrderH')"""  # select name from syscolumns where id=(select max(id) from sysobjects where xtype='u' and name='表名') --读取指定表的所有列名
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return [i[0] for i in results]

    # </editor-fold>
    # <editor-fold desc="查询表的值">
    def select_value(self, sql=None):
        sql1 = '''select TOP 10 * from OrderDS order by iAutoID DESC '''
        sql2 = '''select TOP 10 * from OrderH order by dOrderDate DESC '''
        # sql = '''select * from OrderDS order by cColorCode ASC '''
        self.cursor.execute(sql1)  # 此处输入sql
        rows1 = self.cursor.fetchall()  # 返回查询的结果
        self.cursor.execute(sql2)  # 此处输入sql
        rows2 = self.cursor.fetchall()  # 返回查询的结果
        return {"OrderDS": rows1, "OrderH": rows2}

    # </editor-fold>
    def close(self):
        self.cursor.close()
        self.conn.close()

    def executemany_start(self, OrderDS_lis, OrderH_tuple, danhao, ):
        # OrderDS_lis = [('1657', 0, 498, 498, 121, 100, 1, 'XL', 1, 'ACEOC111300002', 1, '12135131KZ', '2021-11-30'),
        #          ('1657', 0, 498, 498, 121, 100, 1, 'L', 2, 'ACEOC111300002', 1, '12135131KZ', '2021-11-30'),
        #          ('1657', 0, 498, 498, 121, 100, 1, 'M', 3, 'ACEOC111300002', 1, '12135131KZ', '2021-11-30'),
        #          ('1657', 0, 498, 498, 121, 100, 1, 'S', 4, 'ACEOC111300002', 1, '12135131KZ', '2021-11-30'),
        #          ('0137', 0, 668, 668, 154, 154, 1, '40', 5, 'ACEOC111300002', 2, '120860A', '2021-11-30'),
        #          ('0202', 0, 668, 668, 154, 154, 1, '41', 6, 'ACEOC111300002', 2, '120860A', '2021-11-30'),
        #          ('0614', 0, 668, 668, 154, 154, 1, '42', 7, 'ACEOC111300002', 2, '120860A', '2021-11-30')]
        print(OrderDS_lis, len(OrderDS_lis))
        try:
            sql1 = """INSERT INTO OrderDS(cColorCode, cInyard, fCardPrice, fBalPrice, fCostPrice, cSizeName, iQuantity, cOrderCode,iDisplayIndex,cInvCode, dPreEndDate) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s)"""
            self.cursor.executemany(sql1, OrderDS_lis)
            self.conn.commit()
            # print('批量成功')
        except Exception as e:
            self.conn.rollback()
            self.write_log.write_log_to_Text('OrderDS-插入数据报错——{0}'.format(str(e)), 'red')
        sql2 = """INSERT INTO OrderH(cOrderCode, cFromBraCode, cToBraCode, dOrderDate, fSubscriptionRate, cPriceType, iBraClass,iFlagClass,iSource,bCite, cCreator, dCreateDate, cRevisor, dReviseDate, bPAudit, bFAudit, cMemo, bPayOff) VALUES ('%s','%s', '%s', '%s', '%s','%s', '%s', '%s', '%s',  '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" % \
               OrderH_tuple[0]
        # print(sql2)
        # sql2 = sql2.encode('cp936')
        # sql2 = sql2.encode('gbk')
        try:
            # self.cursor.execute(sql2)
            # self.conn.commit()
            pass
        except Exception as e:
            self.conn.rollback()
            self.write_log.write_log_to_Text('OrderH-插入数据报错——{0}'.format(str(e)), 'red')
            self.close()

    def select_last_orderCode(self):
        sql1 = '''select TOP 1 * from OrderH  order by dOrderDate DESC'''
        self.cursor.execute(sql1)  # 此处输入sql
        rows1 = self.cursor.fetchall()  # 返回查询的结果
        cOrderCode = rows1[0].get("cOrderCode")
        self.write_log.write_log_to_Text(
            '连接数据库,根据OrderH表中的dOrderDate字段倒叙查询出最后一个cOrderCode为{0}....'.format(str(cOrderCode)), 'blue')
        return cOrderCode
