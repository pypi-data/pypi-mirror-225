#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:skyoceanchen
# project_name:automaticoffice
# py_name :acx-21
# software: PyCharm
# datetime:2021/8/6 9:39


import pyodbc  # pyodbc-4.0.32


class Pyodbc_SQLServer(object):
    def __init__(self, write_log=None):
        try:
            self.conn = pyodbc.connect(
                'DRIVER={SQL Server};SERVER=39.108.174.172,8081;DATABASE=JHWData;UID=sa;PWD=@Pursun2018.')
            self.cursor = self.conn.cursor(
            )
            self.write_log = write_log
            if self.cursor:
                write_log.write_log_to_Text('连接数据库成功，可以插入....', 'blue')
            else:
                self.write_log.write_log_to_Text('连接数据库失败，程序崩溃，请联系开发者....', 'red')
        except Exception as e:
            self.write_log.write_log_to_Text('连接数据库失败，程序崩溃，请联系开发者....{0}'.format(str(e)), 'red')

    def select_value(self, sql=None):
        sql1 = '''select TOP 10 * from OrderDS order by iAutoID DESC '''
        sql2 = '''select TOP 10 * from OrderH order by dOrderDate DESC '''
        # sql = '''select * from OrderDS order by cColorCode ASC '''
        self.cursor.execute(sql1)  # 此处输入sql
        rows1 = self.cursor.fetchall()  # 返回查询的结果
        self.cursor.execute(sql2)  # 此处输入sql
        rows2 = self.cursor.fetchall()  # 返回查询的结果
        return {"OrderDS": rows1, "OrderH": rows2}

    def close(self):
        self.cursor.close()
        self.conn.close()

    def executemany_start(self, OrderDS_lis, OrderH_tuple, danhao):
        sql2 = """INSERT INTO OrderH(cOrderCode, cFromBraCode, cToBraCode, dOrderDate, fSubscriptionRate, cPriceType, iBraClass,iFlagClass,iSource,bCite, cCreator, dCreateDate, cRevisor, dReviseDate, bPAudit, bFAudit, cMemo, bPayOff) VALUES ('%s','%s', '%s', '%s', '%s','%s', '%s', '%s', '%s',  '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" % \
               OrderH_tuple[0]
        try:
            self.cursor.execute(sql2)
            self.conn.commit()
            pass
        except Exception as e:
            self.conn.rollback()
            self.write_log.write_log_to_Text('OrderH-单号{0}插入数据报错——原因：{1}'.format(str(danhao), str(e)), 'red')
            self.close()
            return True
        try:
            sql1 = """INSERT INTO OrderDS(cColorCode, cInyard, fCardPrice, fBalPrice, fCostPrice, cSizeName, iQuantity, cOrderCode,iDisplayIndex,cInvCode, dPreEndDate) VALUES ('%s','%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s')"""
            for lis in OrderDS_lis:
                self.cursor.execute(sql1 % lis)
                self.conn.commit()
                pass
            # sql1 = """INSERT INTO OrderDS(cColorCode, cInyard, fCardPrice, fBalPrice, fCostPrice, cSizeName, iQuantity, cOrderCode,iDisplayIndex,cInvCode, dPreEndDate) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s)"""
            # sql1 = """INSERT INTO OrderDS(cColorCode, cInyard, fCardPrice, fBalPrice, fCostPrice, cSizeName, iQuantity, cOrderCode,iDisplayIndex,cInvCode, dPreEndDate) VALUES (?,?,?,?,?,?,?,?,?,?,?)"""
            # self.cursor.executemany(sql1, OrderDS_lis)
            # self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            self.write_log.write_log_to_Text('OrderDS-单号{0}插入数据报错——原因：{1}'.format(str(danhao), str(e)), 'red')
            self.close()
            return True

    def select_last_orderCode(self):
        sql1 = '''select TOP 1 * from OrderH  order by dCreateDate DESC'''
        self.cursor.execute(sql1)  # 此处输入sql
        rows1 = list(self.cursor.fetchone())  # 返回查询的结果
        cOrderCode = rows1[0]
        self.write_log.write_log_to_Text(
            '连接数据库,根据OrderH表中的dCreateDate字段倒叙查询出最后一个cOrderCode为{0}....'.format(str(cOrderCode)), 'blue')
        return cOrderCode
