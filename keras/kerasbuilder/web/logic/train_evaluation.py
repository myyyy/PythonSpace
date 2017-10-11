# -*- coding:utf-8 -*-

from bson import ObjectId
import json
import time
import numpy as np

import tornado
from kpages import url
from mongo_util import MongoIns
from tornado import template

from logic.utility import BaseHandler
from logic.define import *
from logic.excel import *

def data_upload(self):
    code_name = self.get_argument('code_name', '')
    is_del_history = self.get_argument('is_del_history', False)
    model = MongoIns().m_find_one(T_MODEL, code_name=code_name)
    _title = model.get('input',[]).extend(model.get('output',[])) or []
    f = self.request.files['uploadfile'][0]
    body = f.pop('body')
    tmp_filename = '/tmp/' + str(time.time()) + '.xls'
    fd = open(tmp_filename, 'wb')
    fd.write(body)
    fd.close()
    er = ExcelRead(tmp_filename)
    data = er.get_data()
    title = data.pop(0)
    data = np.array(data)
    # data =np.transpose(data)
    result = map(lambda x:dict(zip(title,x)),data)

    uri = self.request.uri.split('/')[1]
    table_name = code_name+'_'+uri
    if is_del_history:
        MongoIns().m_del(table_name)
        for _data in result:
            MongoIns().m_insert(table_name,**_data)
    else:
        for _data in result:
            MongoIns().m_insert(table_name,**_data)

def data_download(self):
    code_name = self.get_argument('code_name', '')
    model = MongoIns().m_find_one(T_MODEL, code_name=code_name)

    uri = self.request.uri.split('/')[1]
    table_name = code_name+'_'+uri
    data, page = MongoIns().m_list(table_name,fields={'_id':0},findall=True)

    _title=[]
    _input = model.get('input',[])
    output = model.get('output',[])
    _title=_input+output

    fname = code_name+"-训练数据(模板).xls"

    if "evaluate"==uri:
        fname = code_name+"-评测数据(模板).xls"

    _data =[]
    for d in data:

        _data.append(map(lambda x:d.get(x,''),_title))
    target_file = ExcelWrite().write(_title, _data)
    self.set_header('Content-Type','application/octet-stream')
    self.set_header('Content-Disposition', 'filename={}'.format(fname))
    self.write(open(target_file).read())
    os.remove(target_file)