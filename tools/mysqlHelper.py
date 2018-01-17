# coding=utf-8
import MySQLdb


class MySqlHelper():
    host='127.0.0.1'
    username = ''
    password = ''
    port=3306
    charset = 'utf8'
    dbname = ''
    executeCursor = None

    connection = None

    def __init__(self):
        pass
    def InitConnectParameter(self,username,password,dbname,host='127.0.0.1',port=3306,charset='utf8'):
        self.username = username
        self.password = password
        self.dbname = dbname
        self.host = host
        self.port = port
        self.charset = charset

    def Connect(self):
        try:
            self.connection = MySQLdb.connect(host=self.host, user=self.username, passwd=self.password, db=self.dbname, port=self.port, charset=self.charset)
            self.connection.ping(True)
            self.executeCursor = self.connection.cursor()
            return True
        except MySQLdb.Error as e:
            print('MySqlHelper.Connect Error：%s' % str(e))
            return False
    def Commit(self):
        try:
            self.connection.commit()
            return True
        except MySQLdb.Error as e:
            print('MySqlHelper.Commit Error：%s' % str(e))
            return False
    def RollBack(self):
        try:
            self.connection.rollback()
            return True
        except MySQLdb.Error as e:
            print('MySqlHelper.RollBack Error：%s' % str(e))
            return False
    def Close(self):
        try:
            self.connection.close()
            return True
        except MySQLdb.Error as e:
            print('MySqlHelper.Close Error：%s' % str(e))
            return False

    def FetchRows(self,sql):
        try:
            cursor = self.connection.cursor()
            print('MySqlHelper.FetchRows Debug：%s' % sql)
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                yield row
        except MySQLdb.Error as e:
            print('MySqlHelper.FetchRows Error：%s \n %s' % (str(e),sql))
            yield None

    def FetchRowsByPage(self,sql,pagesize=0,startpage=0,endpage=0):
        try:
            pageindex = startpage
            while pageindex<=endpage:
                pagesql = sql
                if pagesize > 0:
                    pagesql = sql + ' limit %s,%s' % (pageindex * pagesize, pagesize)
                self.executeCursor.execute(pagesql)
                print('MySqlHelper.FetchRows Debug：%s' % pagesql)
                rows = self.executeCursor.fetchall()
                for row in rows:
                    yield row
                if len(rows)<pagesize or pagesize <= 0:
                    break
                pageindex = pageindex + 1
        except MySQLdb.Error as e:
            print('MySqlHelper.FetchRows Error：%s \n %s' % (str(e),sql))
            #yield None

    def ExecuteScalar(self,sql):
        try:
            self.executeCursor.execute(sql)
            return self.executeCursor[0]
        except MySQLdb.Error as e:
            print('MySqlHelper.OpenScalar Error：%s' % str(e))
            return None

    def ExecuteNonSQL(self,sql,parameters=None):
        try:
            self.executeCursor.execute(sql,parameters)
            return True
        except MySQLdb.Error as e:
            print('MySqlHelper.ExecutNonSQL Error：%s' % str(e))
            return False
