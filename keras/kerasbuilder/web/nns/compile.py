# -*- coding:utf-8 -*-

from bson import ObjectId
import json

import tornado
from kpages import url
from mongo_util import MongoIns
from tornado import template

from logic.utility import BaseHandler
from logic.define import *


@url(r"/optimizer/html")
class OptimizerHtml(BaseHandler):
    def get(self):
        optimizer = self.get_argument('optimizer', '')
        code_name = self.get_argument('code_name', '')
        model = {}
        if code_name:
            model= MongoIns().m_find_one(T_MODEL, code_name=code_name)
            optimizer = model.get('opt',{}).get('optimizer','')
        default = {}
        for opt in OPTIMIZER:
            if opt.get('name')==optimizer:
                default = opt
        path = 'template'
        loader = template.Loader(path)
        html = loader.load('optimizer/optimizer_detail.html').generate(default=default,data=model.get('opt',{}),fix=model.get('fix',{}) )
        self.write(dict(status=True, data=html))

@url(r"/compile/edit")
class CompileEdit(BaseHandler):

    def post(self):
        bind_args = dict((k,v[-1] ) for k, v in self.request.arguments.items())
        bind_args.pop('metrics')
        metrics = self.get_arguments('metrics')
        code_name = bind_args.pop('code_name')
        fix={'loss':bind_args.pop('loss'),'metrics':metrics}
        for k,v in bind_args.items():
            if k=='optimizer':
                continue
            if v.lower() =="false":
                bind_args[k] = False
            elif v.lower() == "true":
                bind_args[k] = True
            else:
                bind_args[k]=float(v)
                print float(v)
        MongoIns().m_update(T_MODEL, {'code_name': code_name}, **{"opt":bind_args,"fix":fix})
        self.write(dict(status=True,data="保存成功"))

