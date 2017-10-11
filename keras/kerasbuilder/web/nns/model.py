# -*- coding:utf-8 -*-

from bson import ObjectId
import json
from zipfile import *
import zipfile
import os

import tornado
from kpages import url
from mongo_util import MongoIns

from logic.utility import BaseHandler
from logic.define import *
from logic import code_render as cr

# @url(r"/index")
@url(r"/")
class Index(BaseHandler):

    def get(self):
        models, _ = MongoIns().m_list(T_MODEL,findall=True)
        self.render('model/model-info.html',models=models,username=self.user_name)

@url(r"/model/data")
class ModelData(BaseHandler):

    def get(self):
        code_name = self.get_argument('code_name')
        model= MongoIns().m_find_one(T_MODEL, code_name=code_name)

        self.write(dict(data=model))

@url(r"/model/data/all")
class ModelDataAll(BaseHandler):

    def get(self):
        models, _ = MongoIns().m_list(T_MODEL,findall=True)
        self.write(json.dumps(models))


@url(r"/model/edit")
class ModelIEdit(BaseHandler):

    def post(self):
        code_name = self.get_argument('code_name')
        name = self.get_argument('name')
        _input = self.get_argument('input').split(',')
        output = self.get_argument('output').split(',')
        model = MongoIns().m_find_one(T_MODEL, code_name=code_name)
        if set(_input)&set(output):
            self.write(dict(status=False,data="输入模型与输出模型不能有相同的名称"))
            return
        num_alarm_set = model.get('num_alarm_set',{})
        new_nas = {}
        print _input
        for i in _input:
            if i in model.get('input'):
                new_nas[i] = num_alarm_set.get(i,[])
            else:
                new_nas[i]=[3,5]

        for i in output:
            if i in model.get('output'):
                new_nas[i] = num_alarm_set.get(i,[])
            else:
                new_nas[i]=[3,5]

        MongoIns().m_update(T_MODEL, {'code_name': code_name}, **{'name':name,'input':_input,'output':output,'num_alarm_set':new_nas})
        self.write(dict(status=True,))

@url(r"/model/download/aipy")
class ModelDownloadAipy(BaseHandler):
    """ 下載aipy文件"""
    def write_csv(self,data,model,csv_file):
        _title=[]
        _input = model.get('input',[])
        output = model.get('output',[])
        _title=_input+output

        csv_data = ''
        for d in data:
            _data = map(lambda x:str(d.get(x,'')),_title)
            csv_data = csv_data+(','.join(_data)+'\n')

        with open(csv_file,'w') as f:
            f.write(csv_data)

    def get(self):
        code_name = self.get_argument('code_name')
        model = MongoIns().m_find_one(T_MODEL, code_name=code_name)
        model_name = model.get('name','')
        ai_data = cr.ai_render(code_name)

        ai_file_name = '{}-ai.py'.format(code_name)
        ai_file = '/tmp/{}'.format(ai_file_name)

        train_table = code_name+'_train'
        evaluate_table = code_name+'_evaluate'
        # train csv文件生成
        data, page = MongoIns().m_list(train_table,fields={'_id':0},findall=True)
        train_csv_file = '/tmp/train-{}.csv'.format(code_name)
        self.write_csv(data,model,train_csv_file)
        # evaluate csv文件生成
        data, page = MongoIns().m_list(evaluate_table,fields={'_id':0},findall=True)
        evaluate_csv_file = '/tmp/evaluate-{}.csv'.format(code_name)
        self.write_csv(data,model,evaluate_csv_file)

        with open(ai_file,'w') as f:
            f.write(ai_data)
        zip_name = '{}-ai.zip'.format(model_name)
        with zipfile.ZipFile('/tmp/{}'.format(zip_name),'w',zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(ai_file)
            zipf.write(train_csv_file)
            zipf.write(evaluate_csv_file)

        self.set_header('Content-Type','application/octet-stream')
        self.set_header('Content-Disposition', 'filename={}'.format(zip_name))

        with open('/tmp/{}'.format(zip_name),'r') as zipf:
            self.write(zipf.read())

@url(r"/model/add")
class ModelAdd(BaseHandler):

    def post(self):
        name = self.get_argument('name')
        code_name = self.get_argument('code_name')
        _input = self.get_argument('input').split(',')
        output = self.get_argument('output').split(',')
        print name
        if set(_input)&set(output):
            self.write(dict(status=False,data="输入模型与输出模型不能有相同的名称"))
            return

        code_name = "nns_"+code_name
        cond = {}
        cond['$or'] = [{'code_name': code_name}, {'name': name}]

        num_alarm_set = dict((i,[3,5]) for i in _input)
        num_alarm_set.update(dict((i,[3,5]) for i in output))

        if not MongoIns().m_find_one(T_MODEL,**cond):
            MongoIns().m_insert(T_MODEL, name=name,code_name=code_name,output=output,input=_input,num_alarm_set=num_alarm_set)
            self.write(dict(status=True,data="添加成功"))
            return
        else:
            self.write(dict(status=False,data="用户名或者代号重复"))


@url(r"/model/del")
class ModelDel(BaseHandler):

    def post(self):
        code_name = self.get_argument('code_name')
        MongoIns().m_del(T_MODEL, code_name=code_name)
        self.write(dict(status=True))
