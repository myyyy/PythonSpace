# -*- coding:utf-8 -*-

from bson import ObjectId
import json
import os
import ast
import time

from kpages import url
from mongo_util import MongoIns
from tornado import template

from logic.utility import BaseHandler
from logic.define import *
from logic import code_render as cr

path = 'template'
loader = template.Loader(path)

def layer_data_convert(layer_name,args):
    params_map = {}
    for lay in LAYER:
        if lay.get('name')==layer_name:
            params_map = dict((p.get('name'),p) for p in lay.get('params'))
    for k,v in args.items():
        if not v:
            args.pop(k)
        if params_map.get(k).get('dt','')=='int' and v:
            args[k] = int(v)
        if params_map.get(k).get('dt','')=='str' and v:
            args[k] = str(v)
        if params_map.get(k).get('dt','')=='bool' and v:
            args[k] =ast.literal_eval(v.capitalize())
        # print params_map.get(k).get('dt','') +'('+v+')'
    return args

@url(r"/layer/add")
class LayerAdd(BaseHandler):
    def post(self):
        bind_args = dict((k, None if v[-1].strip() =="None" else v[-1].strip() ) for k, v in self.request.arguments.items())
        code_name = bind_args.pop('code_name')
        layer_name = bind_args.pop('layer_name')
        bind_args = layer_data_convert(layer_name,bind_args)
        oid = str(ObjectId())
        args = {'layer_name':layer_name,'params':bind_args,'oid':oid}
        MongoIns().m_addToSet(T_MODEL, {'code_name': code_name},**{'struct':args,'struct_order':oid})
        self.write(dict(status=True,data="添加成功"))

@url(r"/layer/edit")
class LayerEdit(BaseHandler):
    def post(self):
        bind_args = dict((k, None if v[-1].strip() =="None" else v[-1].strip() ) for k, v in self.request.arguments.items())
        print bind_args
        code_name = bind_args.pop('code_name')
        oid = bind_args.pop('oid')
        layer_name = bind_args.pop('layer_name')
        bind_args = layer_data_convert(layer_name,bind_args)
        args = {'layer_name':layer_name,'params':bind_args,'oid':oid}
        MongoIns().m_pull(T_MODEL, {'code_name': code_name}, **{'struct': {'oid':oid}})
        MongoIns().m_addToSet(T_MODEL, {'code_name': code_name},**{'struct':args})
        self.write(dict(status=True,data="修改成功"))


@url(r"/layer/edit/order")
class LayerEditOrder(BaseHandler):
    def post(self):
        code_name = self.get_argument('code_name')
        struct_order = self.get_argument('struct_order')
        struct_order = struct_order.split(',')
        MongoIns().m_update(T_MODEL, {'code_name': code_name}, **{'struct_order':struct_order})
        self.write(dict(status=True,data="修改成功"))

@url(r"/layer/del")
class LayerDel(BaseHandler):
    def post(self):
        code_name = self.get_argument('code_name')
        oid = self.get_argument('oid')
        MongoIns().m_pull(T_MODEL, {'code_name': code_name}, **{'struct': {'oid':oid}})
        self.write(dict(status=True,data="刪除成功"))



@url(r"/struct/list/html")
class StructListHtml(BaseHandler):

    def get(self):
        code_name = self.get_argument('code_name')
        model= MongoIns().m_find_one(T_MODEL, code_name=code_name)
        html = loader.load('layer/struct_list.html').generate(data=model)
        imgurl = 'static/keras/{}.png'.format(code_name)
        self.write(dict(status=True, data=html,code=model.get('code',''),imgurl =imgurl ))


@url(r"/layer/html")
class LayerInfo(BaseHandler):
    def get(self):

        oid = self.get_argument('oid','')
        code_name = self.get_argument('code_name','')
        layer_name = self.get_argument('layer_name')
        data = {}
        default = {}
        for lay in LAYER:
            if lay.get('name')==layer_name:
                default = lay
        if oid:
            model = MongoIns().m_find_one(T_MODEL,code_name=code_name)
            for d in model.get('struct',[]):
                if oid == d.get('oid'):
                    data = d.get('params')

        html = loader.load('layer/layer_detail.html').generate(default=default,data=data,oid=oid,code_name=code_name)
        self.write(dict(status=True, data=html))

@url(r"/layer/codeblock/synchro")
class LayerCodeBlockSynchro(BaseHandler):
    """模型结构代码块同步"""

    def get(self):
        code_name = self.get_argument('code_name')
        model = cr.get_model_data(code_name)
        print 'fix',model.get('fix',())
        code = cr.code_render(model.get('struct',()), optimizer=model.get('opt',{}), fix=model.get('fix',()))
        MongoIns().m_update(T_MODEL, {'code_name': code_name}, **{'code':code})
        self.write(dict(status=True, data=code))

@url(r"/layer/codeblock")
class LayerCodeBlock(BaseHandler):
    """模型结构代码块"""

    def get(self):
        code_name = self.get_argument('code_name')
        model = MongoIns().m_find_one(T_MODEL, code_name=code_name)
        self.write(dict(status=True, data=model.get('code','')))

@url(r"/layer/codeview")
class LayerCodeView(BaseHandler):
    """模型结构代码块预览"""
    def get(self):
        code_name = self.get_argument('code_name')
        url = 'static/keras/{}.png?v={}'.format(code_name,time.time())
        md = cr.get_model_data(code_name)
        model = cr.create_model(md.get('struct',[]), optimizer=md.get('opt',{}), fix=md.get('fix',()))
        cr.create_plot(code_name,model)
        self.write(dict(status=True, data=url))

@url(r"/layer/upload")
class LayerUpload(BaseHandler):
    def post(self):
        code_name = self.get_argument('code_name','')
        f = self.request.files['uploadfile'][0]
        body = f.pop('body')
        body = json.loads(body)
        for b in body:
            b['oid'] = str(ObjectId())
            MongoIns().m_addToSet(T_MODEL, {'code_name': code_name},**{'struct':b,'struct_order':b['oid']})
        self.write(dict(status=True,data="添加成功"))

@url(r"/layer/download")
class LayerDownload(BaseHandler):
    def get(self):
        code_name = self.get_argument('code_name')
        model= MongoIns().m_find_one(T_MODEL, code_name=code_name)
        fname = model.get('name','')+"-模型结构.json"
        if model:
            model.pop('_id')
        for item in model.get('struct',[]):
            if item.get('oid',''):
                item.pop('oid')
        struct = json.dumps(model.get('struct',[]), indent=4, sort_keys=False, ensure_ascii=False)
        with open(fname, 'w') as f:
            f.write(struct)
        self.set_header('Content-Type','application/octet-stream')
        self.set_header('Content-Disposition', 'filename={}'.format(fname))
        with open(fname, 'rb') as f:
            self.write(f.read())
        os.remove(fname)
