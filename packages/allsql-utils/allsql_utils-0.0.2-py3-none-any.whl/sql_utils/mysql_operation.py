# -*- coding:utf-8 -*-
"""
@Time : 2022/1/27
@Author : skyoceanchen
@TEL: 18916403796
@File : mysql_operation.py 
@PRODUCT_NAME : PyCharm 
"""
import pymysql  # pip install pymysql==1.1.0


# 操作mysql
class SaveMySQLData(object):

    # <editor-fold desc="连接数据库">
    def __init__(self, host, port, user, password, db, cursorclass=False, charset="utf-8"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset
        self.DictCursor = pymysql.cursors.DictCursor  # 返回字典
        self.cursorclass = cursorclass
        self.conn = None
        self._conn()

    def _conn(self):
        try:
            if self.cursorclass:
                self.conn = pymysql.connect(host=self.host,
                                            port=self.port,
                                            user=self.user,
                                            password=self.password,
                                            db=self.db,
                                            # charset=self.charset,
                                            cursorclass=self.DictCursor
                                            )
            else:
                self.conn = pymysql.connect(host=self.host,
                                            port=self.port,
                                            user=self.user,
                                            password=self.password,
                                            db=self.db,
                                            # charset=self.charset
                                            )
            self.cursor = self.conn.cursor()
            print("数据库连接成功")
            return True
        except Exception as e:
            print("数据库连接失败:" + str(e))
            return False
        # 通过ping()实现数据库的长连接

    def _reConn(self, num=28800, stime=3):
        _status = True
        while _status:
            try:
                # ping校验连接是否异常
                self.conn.ping()
                _status = False
            except:
                print("数据库断开连接，重连")
                if self._conn() == True:
                    _status = False
                    self.cursor = self.conn.cursor()
                    break

                # time.sleep(stime)

    # </editor-fold>
    # <editor-fold desc="新建数据库">
    def create_database(self, db_name):
        """
        :param db_name:数据库名称
        :return:
        """
        self._reConn()
        sql = f'create database if not exists {db_name};'
        self.cursor.execute(sql)
        return db_name

    # </editor-fold>
    # <editor-fold desc="删除数据库">
    def drop_database(self, db_name):
        """
        :param db_name:数据库名称
        :return:
        """
        self._reConn()
        sql = f'drop database if exists {db_name};'
        self.cursor.execute(sql)

    # </editor-fold>
    # <editor-fold desc="查看服务器上的所有数据库">
    def show_databases(self):
        self._reConn()
        sql = 'show databases;'

        return [i[0] for i in self.select(sql)]

    # </editor-fold>
    # <editor-fold desc="查看当前数据库">
    def select_database(self):
        self._reConn()
        sql = 'select database();'
        return self.select(sql)

    # </editor-fold>
    # <editor-fold desc="创建数据表">
    def create_table(self, sql):
        self._reConn()
        # 创建表
        # '''CREATE TABLE COMPANY
        # (
        #     ID INT PRIMARY KEY NOT NULL auto_increment,
        #     NAME TEXT NOT NULL,
        #     AGE INT NOT NULL,
        #     ADDRESS CHAR(50),SALARY REAL,
        #     score float(3,1)
        # );'''
        self.cursor.execute(sql)
        # self.conn.commit()

    # </editor-fold>
    # <editor-fold desc="查看当前数据库中所有的表">
    def show_tables(self):
        self._reConn()
        ''''''
        sql = 'show tables;'
        return [i[0] for i in self.select(sql)]

    # </editor-fold>
    # <editor-fold desc="删除数据库表">
    def drop_table(self, tbl_name):
        self._reConn()
        '''
        :param tbl_name:表名
        :return:
        '''
        sql = f'drop table if exists {tbl_name};'
        self.cursor.execute(sql)

    # </editor-fold>
    # <editor-fold desc="插入数据">
    def insert(self, sql):
        self._reConn()
        """
        :param sql:"INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (1, 'Paul', 32, 'California', 20000.00 )"
        :return:
        """
        """
        sql = "INSERT INTO EMPLOYEE(FIRST_NAME, \
       LAST_NAME, AGE, SEX, INCOME) \
       VALUES ('%s', '%s',  %s,  '%s',  %s)" % \
       ('Mac', 'Mohan', 20, 'M', 2000)
        """
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
            total = self.conn.total_changes
            return total
        except Exception as e:
            # 如果发生错误则回滚
            self.conn.rollback()
            # self.close()

    # </editor-fold>
    # <editor-fold desc="批量插入数据">
    def insert_executemany(self, sql, val):
        self._reConn()
        """
        :param sql:"INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (1, 'Paul', 32, 'California', 20000.00 )"
        :return:
        """
        '''
        data = [['2022-11-07 15:11:23', '077558', '13.4', '22.5', '-1.157', 1],
        ['2022-11-07 15:10:21', '077559', '5.6', '21.4', '-1.844', 3],
        ['2022-11-07 15:10:20', '077560', '10.9', '21.8', '-1.811', 4],
        ['2022-11-07 15:12:13', '077561', '11.5', '22.5', '-1.854', 2]]
        insert_sql = f""" INSERT INTO {waterlevelgauge}(create_time, water_gauge, osmotic_pressure, tem, `value`,info_id)
               VALUES (%s, %s,%s,  %s, %s,  %s);
       """
        '''
        # try:
        #     print("sql", sql)
        #     # 执行sql语句
        #     self.cursor.executemany(sql, val)
        #     # 提交到数据库执行
        #     self.conn.commit()
        # except Exception as e:
        #     print(e)
        #     self.conn.rollback()
        # 执行sql语句
        self.cursor.executemany(sql, val)
        # 提交到数据库执行
        self.conn.commit()

    # </editor-fold>
    # <editor-fold desc="查询数据">
    def select(self, sql):
        self._reConn()
        """
        :param sql:"SELECT id, name, address, salary  from COMPANY"
        :return:
        """
        # Python查询Mysql使用 fetchone() 方法获取单条数据, 使用fetchall() 方法获取多条数据。
        # fetchone(): 该方法获取下一个查询结果集。结果集是一个对象
        # fetchall(): 接收全部的返回结果行.
        # rowcount: 这是一个只读属性，并返回执行execute()方法后影响的行数。
        self.cursor.execute(sql)
        # 获取所有记录列表
        results = self.cursor.fetchall()
        # self.conn.commit()
        return list(results)

    # </editor-fold>
    # <editor-fold desc="更新数据">
    def update(self, sql, ):
        self._reConn()
        """
        :param sql:"UPDATE COMPANY set SALARY = 25000.00 where ID=1"
        :return:
        """
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
        except:
            # 发生错误时回滚
            self.conn.rollback()
            self.close()

    # </editor-fold>
    # <editor-fold desc="删除数据">
    def delete(self, sql):
        self._reConn()
        """
        :param sql:"DELETE from COMPANY where ID=2;"
        :return:
        """
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 提交修改
            self.conn.commit()
        except:
            # 发生错误时回滚
            self.conn.rollback()
            self.close()

    # </editor-fold>
    # <editor-fold desc="关闭数据库">
    def close(self):
        self._reConn()
        self.conn.close()

    # </editor-fold>
    def select_table_fileds(self, table):
        self._reConn()
        sql = f"""show columns from {table};"""
        """+-------------+----------------------+------+-----+-------------------+-----------------------------+
            | Field       | Type                 | Null | Key | Default           | Extra                       |
            +-------------+----------------------+------+-----+-------------------+-----------------------------+
            | actor_id    | smallint(5) unsigned | NO   | PRI | NULL              | auto_increment              |
            | first_name  | varchar(45)          | NO   |     | NULL              |                             |
            | last_name   | varchar(45)          | NO   | MUL | NULL              |                             |
            | last_update | timestamp            | NO   |     | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP |
            +-------------+----------------------+------+-----+-------------------+-----------------------------+
            4 rows in set (0.00 sec)
        """
        data = self.select(sql)
        data = [i.get("Field") if isinstance(i, dict) else i[0] for i in data]
        return data

    def other_sql(self, key, tables=None, databases=None):
        self._reConn()
        dic = {
            # 查询某一张表中所有字段及注释信息
            # 1: f"""-- select COLUMN_NAME,column_comment from INFORMATION_SCHEMA.Columns where table_name ="{tables}";""",
            1: f"""select COLUMN_NAME,column_comment from INFORMATION_SCHEMA.Columns where table_name=`{tables}`; """,
            # 查询某一张表中的所有字段，字段之间以逗号隔开，进行拼接
            2: f"""select  group_concat(COLUMN_NAME) from INFORMATION_SCHEMA.Columns where table_name = {tables};""",
            3: f"""""",
            4: f"""""",
            5: f"""""",
            6: f"""""",
            7: f"""""",
            8: f"""""",
            9: f"""""",
            10: f"""""",
            11: f"""""",
            12: f"""""",
        }
        return dic.get(key)

    def Permission_sql(self):
        self._reConn()
        """-- 查询权限
        SHOW GRANTS FOR '用户名'@'主机名';
        SHOW GRANTS FOR 'lisi'@'%';
        -- 授予权限
        grant 权限列表 on 数据库名.表名 to '用户名'@'主机名';

        -- 给张三用户授予所有权限，在任意数据库任意表上
        GRANT ALL ON *.* TO 'zhangsan'@'localhost';
        -- 撤销权限：
        revoke 权限列表 on 数据库名.表名 from '用户名'@'主机名';
        REVOKE UPDATE ON db3.`account` FROM 'lisi'@'%';

        管理用户
        添加用户
        语法：CREATE USER '用户名'@'主机名' IDENTIFIED BY '密码';
        删除用户
        语法：DROP USER '用户名'@'主机名';
        """
        dic = {
            1: f"""""",
            2: f"""""",
            3: f"""""",
            4: f"""""",
            5: f"""""",
            6: f"""""",
            7: f"""""",
            8: f"""""",
            9: f"""""",
            10: f"""""",
            11: f"""""",
            12: f"""""",
        }

    # </editor-fold>


# cursor = SaveMySQLData(host='localhost', port=3306, user='root', password='root', db='mohe_pro')
# databases = cursor.show_databases()
# print(databases)
"""
导出整个数据库  
mysqldump -u 用户名 -p –default-character-set=latin1 数据库名 > 导出的文件名(数据库默认编码是latin1)  
mysqldump -u wcnc -p smgp_apps_wcnc > wcnc.sql  
2.导出一个表  
mysqldump -u 用户名 -p 数据库名 表名> 导出的文件名  
mysqldump -u wcnc -p smgp_apps_wcnc users> wcnc_users.sql  
3.导出一个数据库结构  
mysqldump -u wcnc -p -d –add-drop-table smgp_apps_wcnc >d:wcnc_db.sql  
-d 没有数据 –add-drop-table 在每个create语句之前增加一个drop table   
4.导入数据库  
A:常用source 命令  
进入mysql数据库控制台，  如mysql -u root -p  
mysql>use 数据库  
然后使用source命令，后面参数为脚本文件(如这里用到的.sql)  
mysql>source wcnc_db.sql  
B:使用mysqldump命令  
mysqldump -u username -p dbname < filename.sql  
C:使用mysql命令  
mysql -u username -p -D dbname < filename.sql  
"""
