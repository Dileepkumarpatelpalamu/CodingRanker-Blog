import mysql.connector
class Posts:
    def __init__(self):
        self.conn= mysql.connector.connect(host="localhost",port="3307",user="root",password="",database="flaskblog")
    def cursor(self):
        self.cursor= self.conn.cursor()
    def closed(self):
        self.conn.close()
    def getposts(self,table):
        qry="SELECT * FROM %s"%(table)
        self.cursor.execute(qry)
        record=self.cursor.fetchall()
        return record
if __name__=='__main__':
    user=Posts()
    user.cursor()
    record=user.getposts("post")
    user.closed()
    
