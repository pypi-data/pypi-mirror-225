# -*- coding:utf-8 -*-
"""
@Time : 2022/1/27
@Author : skyoceanchen

@TEL: 18916403796
@File : sqlite_operation.py 
@PRODUCT_NAME : PyCharm 
"""
import sqlite3


# <editor-fold desc="sqlite">
class SaveSqliteData(object):
    def __init__(self, path):
        """
        :param path:sqlite 文件地址
        """
        # 连接到一个现有的数据库。如果数据库不存在，那么它就会被创建，最后将返回一个数据库对象
        # 该 API 打开一个到 SQLite 数据库文件 database 的链接。
        # 您可以使用 ":memory:" 来在 RAM 中打开一个到 database 的数据库连接，而不是在磁盘上打开。
        # 如果数据库成功打开，则返回一个连接对象。
        # 当一个数据库被多个连接访问，且其中一个修改了数据库，此时 SQLite 数据库被锁定，直到事务提交。
        # timeout 参数表示连接等待锁定的持续时间，直到发生异常断开连接。timeout 参数默认是 5.0（5 秒）。
        # 如果给定的数据库名称 filename 不存在，则该调用将创建一个数据库。
        # 如果您不想在当前目录中创建数据库，那么您可以指定带有路径的文件名，这样您就能在任意地方创建数据库。
        # self.conn = sqlite3.connect(path, timeout=None, detect_types=None, isolation_level=None, check_same_thread=None, factory=None, cached_statements=None, uri=None)
        self.conn = sqlite3.connect(database=path, timeout=5)
        # 该例程创建一个 cursor，将在 Python 数据库编程中用到。该方法接受一个单一的可选的参数 cursorClass。
        # 如果提供了该参数，则它必须是一个扩展自 sqlite3.Cursor 的自定义的 cursor 类。
        self.cursor = self.conn.cursor()

    def create_table(self, sql):
        # 创建表
        '''CREATE TABLE COMPANY
        (
             ID integer PRIMARY KEY autoincrement, #自增组件
            NAME TEXT NOT NULL,
            AGE INT NOT NULL,
            ADDRESS CHAR(50),SALARY REAL
        );'''
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            return False

    # <editor-fold desc="查看当前数据库中所有的表">
    def show_tables(self):
        ''''''
        sql = 'select name from sqlite_master where type=`table` order by name;'
        return self.select(sql)

    # </editor-fold>
    # <editor-fold desc="删除数据库表">
    def drop_table(self, tbl_name):
        '''
        :param tbl_name:表名
        :return:
        '''
        sql = f'drop table if exists {tbl_name};'
        self.cursor.execute(sql)

    # </editor-fold>
    # <editor-fold desc="插入数据">
    def insert(self, sql):
        """
        :param sql:"INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (1, 'Paul', 32, 'California', 20000.00 )"
        :return:
        """
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()

    # </editor-fold>
    # <editor-fold desc="批量插入数据">
    def insert_executemany(self, sql, val):
        """
        :param sql:"INSERT  INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (1, 'Paul', 32, 'California', 20000.00 )"
        :return:
        """
        # 不过 sql 稍微有点区别的是，sqlite 是使用的 ? 作为占位符，而不是 %s，%d 之类的哟！正确方法的例子如下：
        """
        sql = "INSERT INTO EMPLOYEE(FIRST_NAME, \
       LAST_NAME, AGE, SEX, INCOME) \
       VALUES (?,?,?,?,?)" % \
       ('Mac', 'Mohan', 20, 'M', 2000)
        """
        try:
            # 执行sql语句
            self.cursor.executemany(sql, val)
            # 提交到数据库执行
            self.conn.commit()
        except Exception as e:
            print("insert_executemany", e)
            self.conn.rollback()

    # </editor-fold>
    # <editor-fold desc="选择数据">
    def select(self, sql):
        """
        :param sql:"SELECT id, name, address, salary  from COMPANY"
        :return:
        """
        try:
            data = self.cursor.execute(sql)
            # self.conn.commit()
            return list(data)
        except Exception as e:
            pass

    def dict_factory(self, row):
        d = {}
        for idx, col in enumerate(self.cursor.description):
            d[col[0]] = row[idx]
        return d

    def select_dic(self, sql):
        """
        :param sql:"SELECT id, name, address, salary  from COMPANY"
        :return:
        """
        list_data = []
        data = self.cursor.execute(sql)
        for dat in data:
            text = {}
            # 使用cursor游标的description方法，得到数据库的每一列的信息
            # 将data信息与其拼接为字典，并存放入列表中
            # 其实还有个数据库方法获取列名信息：PRAGMA TABLE INOF([表名])
            for s, x in enumerate(self.cursor.description):
                text[x[0]] = dat[s]
            # 若是多个引用值，list.append(str(text))
            list_data.append(text)
        # self.conn.commit()
        return list_data

    # </editor-fold>
    # <editor-fold desc="更新数据">
    def update(self, sql):
        """
        :param sql:"UPDATE COMPANY set SALARY = 25000.00 where ID=1"
        :return:
        """
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()

    # </editor-fold>
    # <editor-fold desc="删除数据">
    def delete(self, sql):
        """
        :param sql:"DELETE from COMPANY where ID=2;"
        :return:
        """
        self.cursor.execute(sql)
        self.conn.commit()

    # </editor-fold>
    # <editor-fold desc="获取表中的所有字段">
    def get_table_fields(self, table_name):
        self.cursor.execute("select * from %s" % table_name)
        col_name_list = [tuple[0] for tuple in self.cursor.description]
        # print(col_name_list)
        return col_name_list

    # </editor-fold>
    # <editor-fold desc="关闭数据库">
    def close(self):
        self.conn.close()
    # </editor-fold>

# </editor-fold>
