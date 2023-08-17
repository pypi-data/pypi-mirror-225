import psycopg2

class PostgreSQL(object):

    def __init__(self, database="szx", user_name="postgres", password="root", host="47.110.58.23", port="15432"):
        self.database = database
        self.user_name = user_name
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.cursor = None
        self.cursor = None

    def connect_host(self):
        """创建连接并启用游标"""
        self.conn = psycopg2.connect(database=self.database,
                                    user=self.user_name,
                                    password=self.password,
                                    host=self.host,
                                    port=self.port)

        self.cursor = self.conn.cursor()


    def execute_select_sql(self, sql=None, flat=None, msg=None):
        """
        查询数据库方法
        有flat时去除列表内元组，只有查询单字段sql可用,否则数据缺失，返回无元组列表
        """
        data = []
        if not self.conn:
            raise ConnectionError('未连接状态，是否未使用connect_host方法连接数据库并创建游标，请连接后重试')
        if sql and flat:
            self.cursor.execute(sql, msg)
            return [i[0] for i in self.cursor.fetchall()]
        elif sql:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        else:
            return data


    def close_connect(self):
        """关闭连接"""
        self.cursor = None
        self.conn.close()
        self.conn = None

    @staticmethod
    def dictfetchall(cursor):
        """
            以字典格式返回数据
        :param cursor:
        :return:
        """
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]
    def query(self, sql, params: list):
        """
            手动查询sql
        :param sql:
        :param params:
        :return:
        """
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        result = self.dictfetchall(cursor)
        self.conn.commit()
        self.conn.close()
        return result
if __name__ == '__main__':
    pass
    # pg = PostgreSQL()
    # pg.connect_host()
    # data_list = pg.execute_select_sql(sql="SELECT shape from part", flat=True)
    # pg.close_connect()