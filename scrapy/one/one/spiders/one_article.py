# -*- coding: utf-8 -*-
import scrapy
import StringIO

import qiniu.config
from qiniu import Auth, put_file, etag, urlsafe_base64_encode

from setting import*
from one.items import OneArticle

BUCKET_NAME = "onespace"
START_URL = 'http://wufazhuce.com/article/'
def qiuniu_upload(localfile,filename):
    q = Auth(ACCESS_KEY, SECRET_KEY)
    token = q.upload_token(BUCKET_NAME, filename, 3600)
    ret, info = put_file(token, filename, localfile)
    print(info)

class OneArticleSpider(scrapy.spiders.Spider):
    name = "onearticle"
    allowed_domains = ["wufazhuce.com"]
    start_urls = map(lambda x:START_URL+str(x),range(ARTICLE_ITEM))
    # start_urls=['http://wufazhuce.com/article/2522']


    def parse(self, response):
        article_num = response.url.split('/')[-1]
        article = OneArticle()
        article['title'] = response.css('.articulo-titulo::text').extract_first().strip()
        article['author'] = response.css('.articulo-autor::text').extract_first().strip()
        article['description'] = response.css('meta[name=description]::attr(content)').extract_first().strip()
        article['content'] = response.css('.articulo-contenido').xpath('.//descendant::node()').extract()
        with open('/tmp/one_article.md', 'w') as file:
            file.write('> '+article['description']+'\n\n')
            file.write('##'+article['title']+'\n')
            file.write('###'+article['author']+'\n')
            file.write(article['content'])
        filename = '/article/'+str(article_num)+'/'+article['title']+'.md'
        qiuniu_upload('/tmp/one_article.md',filename)
        print '*'*25,'\n',len(article['content']),'\n',article_num,'\n','*'*25
