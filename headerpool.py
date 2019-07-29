import os
class headerpool():
    def __init__(self):
        self.pool = self.refreshpool()

    def refreshpool(self):
        path = os.path.dirname(__file__)
        with open(os.path.join(path, 'user_agent'), 'r') as f:
            list_user_agent = f.readlines()
            list_user_agent = [i.replace('\n', '') for i in list_user_agent]
        pool = [{'User-Agent':i} for i in list_user_agent]
        return pool

    def pickheaders(self):
        if len(self.pool) == 0:
            self.pool = self.refreshpool()
        tempheaders = self.pool.pop()
        return tempheaders

if __name__ == "__main__":
    hp = headerpool()
    print(hp.pickheaders())
