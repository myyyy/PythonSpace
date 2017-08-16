# -*- coding: utf-8 -*-
import scrapy
import StringIO
from one.items import OneArticle

import qiniu.config
from qiniu import Auth, put_file, etag, urlsafe_base64_encode

import sys  
reload(sys)  
sys.setdefaultencoding('utf8')  

BUCKET_NAME = "onesp"
ACCESS_KEY = 'j87XHrZkEVh0IQtQn9BdUlsgll0ncPxZ--HvR-Eb'
SECRET_KEY = '45OiWwBr2iuN8lw9A1QO3-8CIxjfRaN-_jDivaRc'

def qiuniu_upload(localfile,filename):
    q = Auth(ACCESS_KEY, SECRET_KEY)
    token = q.upload_token(BUCKET_NAME, filename, 3600)
    ret, info = put_file(token, filename, localfile)
    print(info)

class OneArticleSpider(scrapy.spiders.Spider):
    name = "onearticle"
    allowed_domains = ["wufazhuce.com"]
    start_urls = [
        "http://wufazhuce.com/article/2725",
    ]

    def parse(self, response):
        article = OneArticle()
        article['title'] = response.css('.articulo-titulo::text').extract_first().strip()
        article['author'] = response.css('.articulo-autor::text').extract_first().strip()
        article['description'] = response.css('meta[name=description]::attr(content)').extract_first().strip()
        article['content'] = response.css('.articulo-contenido').xpath('.//p')
        with open('/tmp/one_article.md', 'w') as file:
            file.write('> '+article['description']+'\n\n')
            file.write('##'+article['title']+'\n')
            file.write('###'+article['author']+'\n')
            for art in article['content']:
                try:
                    file.write(art.css("::text").extract_first()+'\n')
                except Exception as e:
                    pass
        qiuniu_upload('/tmp/one_article.md','test2.md')
        print '11111'
