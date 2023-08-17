import sqlite3



class obj:
    def __init__(self, args):
        self.path = args["path"]
        self.tabName = args["tabName"]
        try:
            id = args["id"]
            self.id = id
        except:
            self.id = "id"
        cols = "`,`".join(args["cols"])
        cols = f"`{cols}`"
        self.cols = cols
        self.cols2 = ",".join(args["cols"])
        cols3 = list("?"*len(args["cols"]))
        cols3 = ",".join(cols3)
        self.cols3 = cols3
        self.Start()
        self.CreatTable()
        self.Close()
        # print(self.id)

    def Start(self):
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()

    def CreatTable(self):
        try:
            sql = f'''
            CREATE TABLE IF NOT EXISTS {self.tabName}(
               `{self.id}` INTEGER PRIMARY KEY,
               {self.cols}
            );
            '''
            self.cursor.execute(sql)
            return 1
        except Exception as e:
            print('>> Creat Error:', e)
            return 0

    def Insert(self,tup):
        try:
            sql = f'''
            INSERT INTO {self.tabName} ( {self.id}, {self.cols2} )
            VALUES
            (NULL, {self.cols3});
           '''
            self.Start()
            self.cursor.execute(sql,tup)
            self.conn.commit()
            self.Close()
            return 1
        except Exception as e:
            print('>> Insert Error:', e)
            return 0

    def Select(self, id):
        self.Start()
        self.cursor.execute(f'''SELECT * from {self.tabName} WHERE {self.id}=(?);''', (id,))
        res = self.cursor.fetchall()
        self.Close()
        return res

    def Close(self):
        self.cursor.close()
        self.conn.close()

    def SelectALL(self):
        self.Start()
        sql = f"SELECT * from {self.tabName};"
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        self.Close()
        return res


if __name__ == '__main__':


    args = {}
    args["path"] = "sql.db"
    args["tabName"] = "tab"
    args["id"] = "序号"
    args["cols"] = ["user","score","update_date"]
    db = DB(args)
    db.Insert(('1', '6',"123456"))
    res = db.SelectALL()
    print(res)
