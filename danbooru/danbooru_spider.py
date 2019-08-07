import sys,os,time

sys.path.append('..')

from htmldownloader import htmldownloader
from dup_manager import dup_manager
from dataoutput import dataoutput
from danbooru.danbooru_parser import  *

class danbooru_spider():
    def __init__(self, datapath = os.path.join('..','..','danbooru_data'),china = False):
        self.dm = dup_manager(name = 'danbooru_picurl',errortable=True,document_path=datapath)
        self.hd = htmldownloader(baseurl='https://danbooru.donmai.us', china = china, timeout = 2)
        self.dp = dataoutput(data_path=datapath)
        self.parser = danbooru_parser()
    def crawler_from_search(self, starturl,documentname):
        nextpg = self.crawl_page(starturl,documentname)
        while nextpg != None:
            nextpg = self.crawl_page(nextpg,documentname)
        print('Mention Complete')
    def crawl_page(self,url,documentname):
        response = self.hd.downloadurl(url,timeout=2, max_iter_time=20)
        if response != None:
            pic_dict = self.parser.parser_artist_page(response)
            for filename, picurl in pic_dict.items():
                if picurl not in self.dm.success:
                    pic_res = self.hd.downloadurl(picurl, timeout=2, max_iter_time=10)
                    if pic_res != None:
                        hash = self.dp.save_file(pic_res.content, filename, documentname=documentname)
                        print('SUCCESS: download {}'.format(filename))
                        self.dm.add_success(picurl, hash)
                    else:
                        print('ERROR: download {}'.format(filename))
                else:
                    self.dm.add_error(picurl)
                    print('Already: download {}'.format(filename))
            print('page done')
            nexpage = self.parser.next_page(response)
            return nexpage
        else:
            print("ERROR: in open page")
            return None
if __name__ == '__main__':
    sp = danbooru_spider()
    starturl = 'https://danbooru.donmai.us/posts?ms=1&page=1&tags=haneru&utf8=%E2%9C%93'
    sp.crawler_from_search(starturl,'haneru')
