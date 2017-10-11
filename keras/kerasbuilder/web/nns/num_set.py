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
@url(r"/num/setting")
class NumSet(BaseHandler):

    def post(self):
        bind_args = dict((k,v[-1] ) for k, v in self.request.arguments.items())
        code_name = bind_args.pop('code_name')
        num_alarm_set={}
        for k ,v in bind_args.items():
            bind_args[k] = map(float,v.split(',')[:2])
            num_alarm_set[k] = map(float,v.split(',')[2:])
        MongoIns().m_update(T_MODEL, {'code_name': code_name}, **{'num_set':bind_args,'num_alarm_set':num_alarm_set})
        self.write(dict(status=True))

@url(r"/num/distill")
class NumDistill(BaseHandler):



    def get(self):
        key = self.get_argument('key')
        code_name = self.get_argument('code_name')
        print code_name
        model = MongoIns().m_find_one(T_MODEL, code_name=code_name)
        title = model.get('input',[])+model.get('output',[])
        if key in title:
            lst = MongoIns().m_distinct(code_name+'_train',key)
        _max=max(lst)
        _min = min(lst)
        num_set = model.get('num_set',{})
        num_set[key] = [float(_min),float(_max)]
        MongoIns().m_update(T_MODEL,{'code_name':code_name},num_set=num_set)
        self.write(dict(status=True,max=_max,min=_min))

@url(r"/num/distill/all")
class NumDistillAll(BaseHandler):



    def get(self):
        code_name = self.get_argument('code_name')
        model = MongoIns().m_find_one(T_MODEL, code_name=code_name)
        keys = model.get('input',[])+model.get('output',[])
        num_set={}
        group ={}
        for key in keys:
            group['_id'] = None
            group.setdefault(key+'_min',{})
            group.setdefault(key+'_max',{})
            group[key+'_min']["$min"] = '$'+key
            group[key+'_max']["$max"] = '$'+key

        pipeline = [
                            {
                                "$group": group
                            },
                ]
        data = MongoIns().m_aggregate(code_name+'_train', pipeline)
        data = data.get('result')[0]
        for key in keys:
            num_set[key] = [data.get(unicode(key)+'_min',''),data.get(unicode(key)+'_max','')]
        MongoIns().m_update(T_MODEL,{'code_name':code_name},num_set=num_set)
        print num_set
        self.write(dict(status=True,data=num_set))

@url(r"/num/data")
class NumData(BaseHandler):

    def get(self):
        code_name = self.get_argument('code_name')
        model = MongoIns().m_find_one(T_MODEL, code_name=code_name)
        self.write(dict(status=True,data=model.get('num_set',{}),num_alarm_set=model.get('num_alarm_set',{})))

@url(r"/num/setdefault")
class NumSetdefault(BaseHandler):

    def get(self):
        code_name = self.get_argument('code_name')
        model = MongoIns().m_find_one(T_MODEL, code_name=code_name)
        title = model.get('input')+model.get('output')
        num_alarm_set = {}
        for key in title:
            num_alarm_set[key]=[3,5]
        data = MongoIns().m_update(T_MODEL,{'code_name':code_name},num_alarm_set=num_alarm_set)
        self.write(dict(status=True,data=data))


