import pymysql
import csv

class Database():
    def __init__(self):
        self.db = pymysql.connect(host='localhost',
                                  user='root',
                                  password='1234',
                                  db='senior_dietplanner',
                                  charset='utf8')
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

csv_data=open('recipe.csv', 'r', encoding='utf-8')
csv_data.readline()
for row in range(csv_data):
    insert_line=row.split(',')
    cursor.execute('insert into recipe values(int(insert_line[0]), "insert_line[1]", "insert_line[2]", "insert_line[3]" ,"insert_line[4]", "insert_line[5]")')
db.commit()
cursor.close()



    # def execute(self, query, args={}):
    #     self.cursor.execute(query, args)
    #
    # def executeOne(self, query, args={}):
    #     self.cursor.execute(query, args)
    #     row = self.cursor.fetchone()
    #     return row
    #
    # def executeAll(self, query, args={}):
    #     self.cursor.execute(query, args)
    #     row = self.cursor.fetchall()
    #     return row
    #
    # def commit():
    #     self.db.commit()
