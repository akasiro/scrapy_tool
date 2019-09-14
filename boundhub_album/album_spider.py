import sys,os,time

sys.path.append('..')

from htmldownloader import htmldownloader
from dup_manager import dup_manager
from dataoutput import dataoutput
from boundhub_album.boundhub_parser import  *
class album_spider():
    def __init__(self,china = True):
        self.dm = dup_manager(name = 'boundhub_pic', document_path=os.path.join('..','..','boundhub_data'))
        self.downloader = htmldownloader(baseurl='https://www.boundhub.com',china = china)
        self.dp = dataoutput(data_path=os.path.join('..','..','boundhub_data'))
        self.parser = boundbub_parser()

    def from_album_url(self,url):
        response = self.downloader.downloadurl(url = url)
        if response == None:
            print('ERROR: fail to open album')
        else:
            result = self.parser.album_parser(response)
            albumname = result[0]
            picurllist = result[1]
            picname_pattern = re.compile('[\d]+.jpg')
            for picurl in picurllist:
                picfilename = re.findall(picname_pattern,picurl)[0]
                if picurl in self.dm.success:
                    print('{:.2f}% | Already {}'.format((picurllist.index(picurl)+1)/len(picurllist)*100, picfilename))
                    break
                picres = self.downloader.downloadurl(picurl,max_iter_time=10, timeout=2)
                if picres != None:
                    pichash = self.dp.save_file(data=picres.content,filename=picfilename,documentname=albumname)
                    self.dm.add_success(picurl,hash = pichash)
                    print('{:.2f}% | SUCCESS in download {}'.format((picurllist.index(picurl)+1)/len(picurllist)*100, picfilename))
                    time.sleep(2)
                else:
                    print('ERROR: fail to download {}'.format(picfilename))
            print('Done')



if __name__ == "__main__":
    sp =album_spider()
    # albumurl = 'https://www.boundhub.com/albums/7780/court-bondage/'
    with open('urllist.txt','r') as f:
        tmp = f.readlines()
    albumlist = [i.replace('\n','') for i in tmp]
    for i in albumlist:
        sp.from_album_url(i)
    print('mission complete')
