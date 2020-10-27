import MySQLdb

class dbConnect():
    def __init__(self):
        # 打开数据库连接
        self.db = MySQLdb.connect(host="tc-mysql-0.services.infra.tree-diagram.site", user="root", password="LMS++dev",
                             db="hdgcSys", port=10034)
        # 使用cursor()方法获取操作游标
        self.cursor = self.db.cursor()
        # 使用execute方法执行SQL语句
        self.cursor.execute("SELECT VERSION()")
        # 使用 fetchone() 方法获取一条数据
        data = self.cursor.fetchone()

        print("Database version : %s " % data)

    def getpassword(self, username_in):
        # SQL 查询语句
        sql = "SELECT password FROM user \
               WHERE username = %s" % username_in
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = self.cursor.fetchall()[0][0]
            print(results)
            return results
        except:
            print
            "Error: unable to fecth data"
        # 关闭数据库连接
        self.db.close()
