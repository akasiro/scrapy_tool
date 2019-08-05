import os,sqlite3
class dataoutput():
    def __init__(self, method, data_path = 'data', db_name = 'data.db'):
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        if method.lower() == 'db':
            self.conn = sqlite3.connect(os.path.join(data_path,db_name))
            self.cur = self.conn.cursor()
    def create_db_table(self,tablename,vardict):
        var_define =','.join(['{} {}'.format(k,v) for k,v in vardict.items()])
        create_tb_cmd = 'create table if not exists {} ({})'.format(tablename,var_define)
        try:
            self.cur.execute(create_tb_cmd)
            self.conn.commit()
            print('SUCCESS: {} create'.format(tablename))
        except:
            print('ERROR: error in creating table in db')

    def insert_data_db(self,tablename,data):
        if type(data) == list:
            data = tuple(data)
        if type(data) == tuple:
            # 检查数据格式是否符合数据表
            # 获取表的列数
            get_columns_cmd = 'pragma table_info({})'.format(tablename)
            self.cur.execute(get_columns_cmd)
            col_name = self.cur.fetchall()
            #  检查数据长度是否相符
            if len(col_name) != len(data):
                print('data len wrong')
            insert_tuple_cmd = 'insert into {} values ({}?)'.format(tablename,'?,'*(len(data)-1))
            try:
                self.cur.execute(insert_tuple_cmd,data)
                self.conn.commit()
            except:
                print('ERROR: error insert')
        elif type(data) == dict:
            insert_dict_cmd = 'insert into {} ({}) values ({}?)'.format(tablename,','.join(list(data.keys())), '?, '*(len(data)-1))
            try:
                self.cur.execute(insert_dict_cmd,tuple(data.values()))
                self.conn.commit()
            except:
                print('ERROR: insert data')
if __name__ == '__main__':
    dp = dataoutput('db', 'test')
    vardict = {'id':'integer primary key autoincrement',
               'name':'varchar(10)'}
    dp.create_db_table('test',vardict)
    datatuple = (None,'qiye')
    datadict = {'name':'cp'}
    dp.insert_data_db('test',datatuple)
    dp.insert_data_db('test',datadict)


