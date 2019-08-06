import sys,os,time

sys.path.append('..')

from htmldownloader import htmldownloader
from dup_manager import dup_manager
from dataoutput import dataoutput
from boundhub_album.boundhub_parser import  *
class album_spider():
    def __init__(self):
        self.dm = dup_manager(name = 'boundhub_pic', errortable=True, newtable= True)
        self.downloader = htmldownloader(baseurl='https://www.boundhub.com',china = False)
        self.dp = dataoutput()
        self.parser = boundbub_parser()

    def from_album_url(self,url):
        response = self.downloader.downloadurl(url = url)
        result = self.parser.album_parser(response)
        albumname = result[0]
        picurllist = result[1]
        picname_pattern = re.compile('[\d]+.jpg')
        filepath = os.path.join('..','..','boundhub_data',albumname)
        for picurl in picurllist:
            picfilename = re.findall(picname_pattern,picurl)[0]
            picres = self.downloader.downloadurl(picurl)
            pichash = self.dp.save_file(picres.content,filepath,picfilename)
            self.dm.add_success(picfilename,hash = pichash)
            time.sleep(2)
        print('Done')



if __name__ == "__main__":
    sp =album_spider()
    albumurl = 'https://www.boundhub.com/albums/7780/court-bondage/'
    sp.from_album_url(albumurl)
