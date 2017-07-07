# -*- coding:utf-8 -*-
"""
    plat action
    author suyf
"""
import time
from tornado.web import stream_request_body
import tornado.web
from bson import ObjectId
from bson import Binary

from kpages import url

from mongo_util import MongoIns;mongo_util = MongoIns()
from logic.utility import ActionHandler
from logic.utility import BaseSocketHandler
# 文件大小参数
MB = 1024 * 1024
GB = 1024 * MB
TB = 1024 * GB
MAX_STREAMED_SIZE = 1*GB

@url(r'/sensor/data/upload')
class SensorDataUpload(ActionHandler):
    """数据上传.大文件上传"""
    def get(self):
        gfs = mongo_util.get_gfs().get(ObjectId("595e0caf4d4b2509fca839ad"))
        # import pdb;pdb.set_trace()
        self.set_header('Content-Type',gfs.contentType)
        self.set_header('Content-Disposition', 'filename={}'.format(gfs.name))
        self.write(gfs.read())

    def prepare(self):
        self.request.connection.set_max_body_size(MAX_STREAMED_SIZE)

    def post(self):
        t1 = time.time()
        chunk_num = int(self.get_argument('chunks'))
        file_size = int(self.get_argument('size'))
        chunk_tip = int(self.get_argument('chunk'))
        file_id = self.get_argument('guid')
        filename =self.get_argument('name')
        content_type = self.get_argument('type')
        chunk_data = self.request.body
        if chunk_tip ==0:
            mongo_util.m_insert('fs.files', dbname = 'sensorcmd',
                **{ 
                "_id" :ObjectId(),
                "fid":file_id,
                "filename" : filename,
                "length" :file_size,
                "chunkSize" : len(chunk_data),
                "uploadDate" : time.time(),
                "md5" : None, 
                "contentType" : content_type,
                "meta" : None
                })
        gfsid = mongo_util.m_find_one('fs.files', dbname = 'sensorcmd',fid=file_id).get('_id')
        mongo_util.m_insert('fs.chunks', dbname = 'sensorcmd',
            **{ 
            "_id" : ObjectId(),
            "files_id" : ObjectId(gfsid),
            "n" : chunk_tip,
            "data" : Binary(chunk_data)
            })
        if chunk_tip+1 ==chunk_num:
            mongo_util.m_update('fs.files',{'_id':ObjectId(gfsid),},dbname = 'sensorcmd',finished=True)
        data = Binary(self.request.uri)
        print time.time()-t1,chunk_tip
        self.write(dict(status=True,data='上传成功'))


@url(r'/sensor/data/download')
class SensorDataDownload(tornado.web.RequestHandler):
    """数据下载"""
    def get(self):
        file_name=''
        file_path = ''
        self.set_header('Content-Type','application/octet-stream')
        self.set_header('Content-Disposition', 'filename={}'.format(file_name))
        with open(file_path) as f:
            self.write(f.read())



@url(r"/sensor/data/upload/ws")
class WebSocketHandler(BaseSocketHandler):

    def on_message(self, message):
        self.write_message(u"Your message was: "+message)  