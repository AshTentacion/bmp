import pymysql
import datetime
import re

class Db:
    db = None
    cursor = None

    @staticmethod
    def table_exists(con, table_name):
        sql = "show tables;"
        con.execute(sql)
        tables = [con.fetchall()]
        table_list = re.findall('(\'.*?\')', str(tables))
        table_list = [re.sub("'", '', each) for each in table_list]
        if table_name in table_list:
            return 1
        else:
            return 0

    @staticmethod
    def check_conn(cursor):
        if cursor is None:
            print("you have wrong connection")
        return cursor is None

    def __init__(self):
        self.db = pymysql.connect('localhost', 'root', '123', 'test_db')
        if self.db is None:
            print("Connect error")
        else:
            self.cursor = self.db.cursor()
            if self.cursor is not None:
                print("Connect ok")

    def create_table(self):
        if self.check_conn(self.cursor):
            return
        if self.table_exists(self.cursor, 'bmp280'):
            print("table existed")
            return
        self.cursor.execute("DROP TABLE IF EXISTS bmp280")
        sql = '''
            CREATE TABLE `bmp280` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `temp` float DEFAULT NULL,
            `pressure` float DEFAULT NULL,
            `time` datetime DEFAULT NULL,
            `creator` varchar(45) DEFAULT NULL,
            PRIMARY KEY (`id`)
            ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
        '''
        res = self.cursor.execute(sql)
        self.db.commit();

    def insert(self, data):
        if self.check_conn(self.cursor):
            return
        sql = 'insert into bmp280(temp,pressure,time,creator) ' \
              'values(%s, %s, %s, %s)'
        res = self.cursor.execute(sql, data)
        self.db.commit()
        print("insert res"+str(res))

    def select_all(self):
        if self.check_conn(self.cursor):
            return
        sql = 'select * from bmp280'
        count = self.cursor.execute(sql)
        print('count' + str(count))
        res = self.cursor.fetchall()
        self.db.commit()
        return res

    def destroy(self):
        self.cursor.close()
        self.db.close()


def test():
    db = Db()
    db.create_table()
    create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = [23, 3223, create_time, 'tester']
    db.insert(data)
    print(db.select_all())
    db.destroy()


if __name__ == '__main__':
    test()
