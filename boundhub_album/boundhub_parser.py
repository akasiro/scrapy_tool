import re
class boundbub_parser():
    def album_parser(self, album_res):
        html = album_res.text
        picurl_pattern = 'https://www.boundhub.com/get_image/2/[\w]+/sources/[\w]+/[\w]+/[\d]+.jpg/'
        title_pattern = '<title>[\s\S]+</title>'
        picurls = re.findall(re.compile(picurl_pattern),html)
        title = re.findall(re.compile(title_pattern),html)[0].replace('<title>','').replace('</title>','')
        return [title, picurls]



