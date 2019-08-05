import sqlite3,os,hashlib


class dup_manager():
    def __init__(self,name, type = 'varchar(50)',newlist = [], errortable = False, newtable = False, document_path = ''):
        self.conn = sqlite3.connect(os.path.join(document_path,'duplicate_check.db'))
        self.cur = self.conn.cursor()
        self.name = name
        # 创建3个表
        # 1.创建已经完成的表
        self.success = set()
        try:
            self.cur.execute('create table {}_success (id integer primary key autoincrement, {} {}, hash varchar(100))'.format(name,name,type))
            self.conn.commit()
        except:
            self.cur.execute('select {} from {}_success'.format(name,name))
            res1 = self.cur.fetchone()
            if res1 != None:
                self.success = set(res1)
                self.cur.execute('select hash from {}_success'.format(name))
                res2 = self.cur.fetchone()
                self.success_hash = set(res2)


        # 2.创建出错的表

        if errortable:
            self.error = set()
            try:
                self.cur.execute('create table {}_error (id integer primary key autoincrement, {} {} )'.format(name,name,type))
                self.conn.commit()
            except:
                self.cur.execute('select {} from {}_error'.format(name,name))
                res3 = self.cur.fetchone()
                if res3 != None:
                    self.error = set(res3)

        # 3.创建等待处理的表
        self.new = set()
        if newtable:
            self.new = set(newlist)
            try:
                self.cur.execute('create table {}_new (id integer primary key autoincrement, {} {} )'.format(name, name, type))
                self.conn.commit()
            except:
                self.cur.execute('select {} from {}_new'.format(name, name))
                res4 = self.cur.fetchone()
                if res4 != None:
                    self.new = self.new | set(res4)
            # 对new进行去重（去重之后重新建表）
            self.new = self.new-self.success
            if errortable:
                self.new = self.new - self.error
            self.cur.execute('drop table {}_new'.format(name))
            self.conn.commit()
            self.cur.execute('create table {}_new (id integer primary key autoincrement, {} {} )'.format(name, name, type))
            self.conn.commit()
            for i in self.new:
                self.cur.execute('insert into {}_new values (?,?)'.format(name), (None,i))
                self.conn.commit()

    def has_new(self):
        return self.new_size != 0

    def new_size(self):
        return len(self.new)

    def get_new(self):
        return self.new.pop()

    def add_new(self, newthing):
        if self.error in dir():
            temp = self.error | self.success | self.new
        else:
            temp = self.success | self.new
        if newthing not in temp:
            self.new.add(newthing)
            try:
                self.cur.execute('insert into {}_new values (?,?)'.format(self.name), (None,newthing))
                self.conn.commit()
            except:
                pass
    def add_new_list(self,newlist):
        for i in newlist:
            self.add_new(i)

    def add_success(self,successthing):
        if successthing not in self.success:
            hash = hashlib.sha256(successthing.encode()).hexdigest()
            try:
                self.cur.execute('insert into {}_success values (?,?,?)'.format(self.name), (None, successthing, hash))
                self.conn.commit()
                self.success.add(successthing)
            except:
                pass
    def add_error(self, errorthing):
        if errorthing not in self.error:
            try:
                self.cur.execute('insert into {}_error values (?,?)'.format(self.name), (None, errorthing))
                self.conn.commit()
                self.error.add(errorthing)
            except:
                pass

    def old_size(self):
        if self.error in dir():
            temp = self.error | self.success
        else:
            temp = self.success
        return len(temp)

if __name__ == "__main__":
    with open('user_agent', 'r') as f:
        temp = [i.replace('\n','') for i in f.readlines()]
    dm = dup_manager('test', newtable=True, errortable=True, newlist= temp)
    dm.add_error(temp[3])
    dm.add_success(temp[4])






