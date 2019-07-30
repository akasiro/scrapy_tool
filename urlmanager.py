class urlmanager():
    def __init__(self):
        self.newurl = set()
        self.errorurl = set()
        self.usedurl = set()

    def has_new_url(self):
        '''
        判断是否还有未爬去的url
        :return:
        '''
        return self.new_url_size() !=0
    def get_new_url(self):
        new_url = self.newurl.pop()
        return new_url

    def add_used_url(self,url):
        self.usedurl.add(url)

    def add_error_url(self,url):
        self.errorurl.add(url)

    def add_new_url(self,url):
        if url not in self.usedurl and url not in self.errorurl:
            self.newurl.add(url)
    def add_new_urls(self,urls):
        for url in urls:
            self.add_new_url(url)

    def new_url_size(self):
        return len(self.newurl)

    def old_url_size(self):
        return len(self.errorurl) + len(self.usedurl)
