import re
from urllib.request import urljoin
class danbooru_parser():
    def parser_artist_page(self,response):
        pic_url_pattern = re.compile('https://danbooru.donmai.us/data/[\w]+.jpg')
        pic_filename_pattern = re.compile('[\w]+.jpg')
        pic_url_list = re.findall(pic_url_pattern,response.text)
        pic_dict = {re.findall(pic_filename_pattern,url)[0]:url for url in pic_url_list}
        return pic_dict

    def next_page(self, response):
        baseurl = 'https://danbooru.donmai.us'
        nextpage_tag_pattern = re.compile('paginator-next')
        nextpage_pattern = re.compile('/posts\?[\w=]+&page=[\w&%=]+')
        if len(re.findall(nextpage_tag_pattern, response.text)) != 0:
            nextpageurl = re.findall(nextpage_pattern,response.text)[0]
            nextpageurl_full = urljoin(baseurl,nextpageurl)
        else:
            nextpageurl_full = None
        return nextpageurl_full

