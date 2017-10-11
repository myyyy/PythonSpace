# -*- coding:utf-8 -*-

from bson import ObjectId
import json
import time
import numpy as np
import copy
import ast
import psutil

import tornado
from kpages import url,service_async
from mongo_util import MongoIns
from tornado import template
import tornado.web
from tornado import gen
from kpages import get_context, srvcmd, util as mongo_util
import motor.motor_tornado

from logic.utility import BaseHandler
from logic.define import *
from logic.excel import *
from logic import train_evaluation as te
from logic import code_render as cr
from setting import DB_HOST, DB_NAME

path = 'template'
loader = template.Loader(path)


@url(r"/train/edit")
@url(r"/evaluate/edit")
class TrainEvaluateEdit(BaseHandler):
    """训练数据编辑"""

    def get(self):
        code_name = self.get_argument("code_name")
        _id = self.get_argument("_id")
        model = MongoIns().m_find_one(T_MODEL, code_name=code_name)
        _title = []
        _input = model.get('input', [])
        output = model.get('output', [])
        _title = _input+output
        uri = self.request.uri.split('/')[1]
        table_name = code_name+'_'+uri
        train = MongoIns().m_find_one(table_name, _id=ObjectId(_id))

        self.write(dict(status=True, data=train, title=_title))

    def post(self):
        bind_args = dict((k, v[-1]) for k, v in self.request.arguments.items())
        code_name = bind_args.pop("code_name")
        _id = bind_args.pop("_id")

        uri = self.request.uri.split('/')[1]
        table_name = code_name+'_'+uri

        MongoIns().m_update(table_name, {'_id': ObjectId(_id)}, **bind_args)
        self.write(dict(status=True, data="编辑成功"))


@url(r"/train/del")
@url(r"/evaluate/del")
class TrainEvaluateDel(BaseHandler):
    """训练数据删除"""

    def post(self):
        code_name = self.get_argument('code_name')
        ids = self.get_argument('_id').split(',')
        uri = self.request.uri.split('/')[1]
        table_name = code_name+'_'+uri
        for _id in ids:
            MongoIns().m_del(table_name, _id=ObjectId(_id))
        self.write(dict(status=True, data="删除成功"))



@url(r"/train/excel/upload")
@url(r"/evaluate/excel/upload")
class TrainEvaluateExcelUpload(BaseHandler):
    """ 训练数据导入"""

    def post(self):
        te.data_upload(self)
        self.write(dict(status=True, data="导入成功"))


@url(r"/train/excel/download")
@url(r"/evaluate/excel/download")
class TrainEvaluateExcelDownload(BaseHandler):
    """ 训练数据下载"""

    def get(self):
        te.data_download(self)


@url(r"/train/mongo/upload")
@url(r"/evaluate/mongo/upload")
class TrainEvaluateMongoUpload(BaseHandler):
    """ 数据Mongo导入"""
    @tornado.web.asynchronous
    @gen.coroutine
    def post(self):
        bind_args = dict((k, v[-1]) for k, v in self.request.arguments.items())
        code_name = bind_args.pop('code_name')
        url = bind_args.pop('url')
        sql = bind_args.pop('sql', {})
        sql = ast.literal_eval(sql)
        is_del_history = bind_args.pop('is_del_history', False)
        uri = self.request.uri.split('/')[1]
        to_collection = code_name+'_'+uri
        if is_del_history:
            MongoIns().m_del(to_collection)

        url = url.split('/')
        to_uri, from_db, from_collection = url[0], url[1], url[2]

        args = dict(filter(lambda x: x[1] != '', bind_args.items()))
        # keys = args.values()
        # fields=set(bind_args.values())-set([""]) map(lambda x:{x:1},args)
        from_client = motor.motor_tornado.MotorClient(to_uri)
        data = yield from_client[from_db][from_collection].find(sql).to_list(length=None)
        to_client = motor.motor_tornado.MotorClient(DB_HOST)
        for d in data:
            _data = {}
            for k, v in args.items():
                try:
                    _data[k] = float(d.get(v, ''))
                except Exception as e:
                    _data[k] = d.get(v, '')
            if _data:
                yield to_client[DB_NAME][to_collection].insert(_data)

        self.write(dict(status=True, data="导入成功"))


@url(r"/train/list/html")
@url(r"/evaluate/list/html")
class TrainEvaluateListHtml(BaseHandler):

    def get(self):
        code_name = self.get_argument('code_name')

        model = MongoIns().m_find_one(T_MODEL, code_name=code_name)
        _input = model.get('input', [])
        output = model.get('output', [])
        kwargs = {}
        page_index = int(self.get_argument('page_index', 1))
        kwargs['page_size'] = 8
        kwargs['page_index'] = page_index

        uri = self.request.uri.split('/')[1]
        table_name = code_name+'_'+uri

        data, page = MongoIns().m_list(table_name, **kwargs)
        html = loader.load('train/train_list.html').generate(data=data,
                                                             _input=_input, output=output, page=page, uri=uri)
        print data
        self.write(dict(status=True, data=html))
        # self.render('train/train_list.html',data=data,_input = _input,output=output,page=page)


@url(r"/train/setting")
@url(r"/evaluate/setting")
class TrainEvaluateSet(BaseHandler):

    def get(self):
        code_name = self.get_argument('code_name')

        uri = self.request.uri.split('/')[1]
        field_name = uri+"_setting"
        print field_name
        model = MongoIns().m_find_one(T_MODEL, code_name=code_name)
        print model
        self.write(dict(status=True, data=model.get(field_name, {})))


@url(r"/train/setting/edit")
@url(r"/evaluate/setting/edit")
class TrainEvaluateSetEdit(BaseHandler):

    def post(self):
        bind_args = dict((k, v[-1]) for k, v in self.request.arguments.items())
        print bind_args
        code_name = bind_args.pop('code_name')

        uri = self.request.uri.split('/')[1]
        # field_name = uri+"_setting"

        MongoIns().m_update(
            T_MODEL, {'code_name': code_name}, **{'train_setting': bind_args})

        self.write(dict(status=True, data="编辑成功"))


@url(r"/train/exec")
class TrainExec(BaseHandler):
    """ 模型训练"""

    def get(self):
        code_name = self.get_argument('code_name', None)
        model = MongoIns().m_find_one(T_MODEL, code_name=code_name)
        train_pid = model.get('train_pid')
        MongoIns().m_update(T_MODEL, {'code_name':code_name},train_status='0')
        if not psutil.pid_exists(train_pid) or psutil.Process(train_pid).status() == psutil.STATUS_ZOMBIE:
            # MongoIns().m_update(T_MODEL, {'code_name':code_name},train_status='0')
            self.write(dict(status=True,data='已经终止训练'))
            return
        try:
            if psutil.pid_exists(train_pid):
                p = psutil.Process(train_pid)
                p.kill()
                if not psutil.pid_exists(train_pid):
                    # MongoIns().m_update(T_MODEL, {'code_name':code_name},train_status='0')
                    self.write(dict(status=True,data='终止训练成功'))
                    return
        except Exception as e:
            self.write(dict(status=True,data='终止训练失败',e=str(e)))

    def post(self):
        code_name = self.get_argument('code_name', None)
        model = MongoIns().m_find_one(T_MODEL, code_name=code_name)
        train_pid = model.get('train_pid')

        if model.get('train_status','0')=='0':
            MongoIns().m_update(T_MODEL, {'code_name':code_name},train_pid=train_pid,train_status='1')
            service_async('mq_train',{'code_name':code_name})
            self.write(dict(status=True,data='训练指令发送成功'))
            return
        if model.get('train_status','0')=='1':
            self.write(dict(status=True,data='训练正在执行，请等待'))
            return


@url(r"/train/exec/log")
class TrainExecLog(BaseHandler):
    """ 模型训练 后台日志信息输出"""

    def get(self):
        code_name = self.get_argument('code_name', None)
        csv_file = 'static/keras/{}.csv'.format(code_name)
        try:
            data = None
            with open(csv_file,'r') as f:
                data = os.popen('tail -n 20 {}'.format(csv_file))
                title = f.readline()
                _data = data.readlines()
                if title not in _data:
                    _data.insert(0,title)
                self.write(dict(status=True,data=_data,title=title))
        except Exception as e:
            self.write(dict(status=True,data='正在获取日志'))



@url(r"/evaluate/exec")
class EvaluateExec(BaseHandler):
    """ 模型评测"""

    def post(self):
        code_name = self.get_argument('code_name')
        model = MongoIns().m_find_one(T_MODEL, code_name=code_name)
        m = cr.get_model(code_name)
        batch_size = int(model.get('train_setting', {}).get('batch_size', 32))
        _input = model.get('input', [])
        output = model.get('output', [])

        table_name = code_name + '_evaluate'
        lst, page = MongoIns().m_list(table_name, findall=True)
        data = []
        minarray = []
        denoarray =[]
        num_set = model.get('num_set')
        for f in (model.get('input')+model.get('output')):
            f_arr = []
            for node in lst:
                f_arr.append(float(node.get(f, None)))
            data.append(f_arr)
            _min = num_set.get(f)[0]
            _max = num_set.get(f)[1]
            minarray.append(_min)
            denoarray.append(1 if (_max-_min)==0 else (_max-_min))

        data = np.asarray(data)
        data = data.transpose()

        data = cr.normalization_new(data,np.array(minarray),np.array(denoarray))
        trains = data[:, 0:len(model.get('input'))]
        labels = data[:, len(model.get('input')):]
        score = m.evaluate(trains, labels, batch_size=batch_size)
        score = map(lambda x:round(x,4), score)
        print data
        # result = m.predict(trains, batch_size=batch_size, verbose=0)
        # result = result.tolist()
        # for no, r in enumerate(result):
        #     cond = lst[no]
        #     cond.update(zip(output, r))
        #     _id = cond.pop('_id')
        #     MongoIns().m_update(table_name, {'_id': ObjectId(_id)}, **cond)
        MongoIns().m_update(T_MODEL, {'code_name':code_name},loss_value=score[0],metrics_value=score[1])
        self.write(dict(status=True, data="评测成功",score=score))


@url(r"/evaluate/exec/api")
class EvaluateExecApi(BaseHandler):
    """ 模型评测ＡＰＩ"""

    def post(self):
        """
            "args":{
                "code_name": "nns_comger",
                "train_data": [
                    [0,0,0],
                    [0.30000000000000004,0,0.30000000000000004],
                    [0.67,0,0.67]
                ]
            }
        """
        t1 = time.time()
        args = ast.literal_eval(self.get_argument("args"))
        code_name = args.get("code_name")
        data = np.array(args.get("train_data", []))
        model = MongoIns().m_find_one(T_MODEL, code_name=code_name)

        t2 = time.time()
        print t2 - t1

        num_set = model.get('num_set')
        minarray = []
        denoarray =[]
        error_index =set()
        for no, k in enumerate(model.get('input',[])):
            _min = num_set.get(k)[0]
            _max = num_set.get(k)[1]
            for dno,d in enumerate(data):
                if  not (_min<=d[no]<=_max):
                    print k
                    error_index.add(dno)
            minarray.append(_min)
            denoarray.append(1 if (_max-_min)==0 else (_max-_min))
        trains = cr.normalization_new(data,np.array(minarray),np.array(denoarray))
        t3 = time.time()
        print t3 - t2

        m = cr.get_model(code_name)
        t4 = time.time()
        print 'get_model', t4 - t3

        result = m.predict(trains)
        minarray = []
        denoarray =[]
        for k in model.get('output',[]):
            _min = num_set.get(k)[0]
            _max = num_set.get(k)[1]
            minarray.append(_min)
            denoarray.append(1 if (_max-_min)==0 else (_max-_min))
        minarray ,denoarray= np.array(minarray),np.array(denoarray)
        turn_result = cr.turn_normalization(result,minarray,denoarray)

        t5 = time.time()
        print t5 - t4
        self.write(dict(status=True,error_index=list(error_index), data=turn_result.tolist()))


@url(r"/evaluate/exec/score/api")
class EvaluateExecScoreApi(BaseHandler):
    """ 模型评测ＡＰＩ"""

    def post(self):
        """
            "args":{
                "code_name": "nns_comger",
                "train_data": [
                    [0,0,0],
                    [0.30000000000000004,0,0.30000000000000004],
                    [0.67,0,0.67]
                ],
                "label_data": [
                    [0,0],
                    [0.30000000000000004,0],
                    [0.67,0]
                ]
            }
        """
        t1 = time.time()
        args = json.loads(self.get_argument("args"))
        code_name = args.get("code_name")

        trains = np.array(args.get("train_data", []))
        labels = np.array(args.get("label_data", []))

        model = MongoIns().m_find_one(T_MODEL, code_name=code_name)
        num_set = model.get('num_set')
        minarray = []
        denoarray =[]
        for k in model.get('input',[]):
            _min = num_set.get(k)[0]
            _max = num_set.get(k)[1]
            minarray.append(_min)
            denoarray.append(1 if (_max-_min)==0 else (_max-_min))
        trains = cr.normalization_new(trains,np.array(minarray),np.array(denoarray))

        minarray = []
        denoarray =[]
        for k in model.get('output',[]):
            _min = num_set.get(k)[0]
            _max = num_set.get(k)[1]
            minarray.append(_min)
            denoarray.append(1 if (_max-_min)==0 else (_max-_min))
        labels = cr.normalization_new(labels,np.array(minarray),np.array(denoarray))

        m = cr.get_model(code_name)
        score = m.evaluate(trains, labels, batch_size=32)
        val = m.predict(trains)

        self.write(dict(status=True, data=score, val = val.tolist()))


@url(r"/evaluate/exec/alarm")
class EvaluateExecAlarm(BaseHandler):
    """ 模型评测ＡＰＩ"""

    def post(self):
        """
            "args":{
                "code_name": "nns_comger",
                "train_data": [
                    [0,0,0],
                    [0.30000000000000004,0,0.30000000000000004],
                    [0.67,0,0.67]
                ],
                "label_data": [
                    [0,0],
                    [0.30000000000000004,0],
                    [0.67,0]
                ]
            }
        """


        args = json.loads(self.get_argument("args"))
        code_name = args.get("code_name")

        trains = np.array(args.get("train_data", []))
        labels = np.array(args.get("label_data", []))

        model = MongoIns().m_find_one(T_MODEL, code_name=code_name)
        num_set = model.get('num_set')
        num_alarm_set = model.get('num_alarm_set').values()
        std = np.array(model.get('output_std'))
        error_index=set()
        minarray = []
        denoarray =[]
        for no,k in enumerate(model.get('input',[])):
            _min = num_set.get(k)[0]
            _max = num_set.get(k)[1]
            for dno,d in enumerate(trains):
                if  not (_min<=d[no]<=_max):
                    print k
                    error_index.add(dno)
            minarray.append(_min)
            denoarray.append(1 if (_max-_min)==0 else (_max-_min))

        minarray ,denoarray= np.array(minarray),np.array(denoarray)
        trains = cr.normalization_new(trains,minarray,denoarray)
        turn_trains = cr.turn_normalization(trains,minarray,denoarray)

        minarray = []
        denoarray =[]
        # for k,v in num_set.items():
        #     if k in model.get('output',[]):
        #         minarray.append(v[0])
        #         denoarray.append(1 if (v[1]-v[0])==0 else (v[1]-v[0]))
        for k in model.get('output',[]):
            _min = num_set.get(k)[0]
            _max = num_set.get(k)[1]
            minarray.append(_min)
            denoarray.append(1 if (_max-_min)==0 else (_max-_min))
        minarray = np.array(minarray)
        denoarray= np.array(denoarray)
        labels = cr.normalization_new(labels,minarray,denoarray)
        m = cr.get_model(code_name)
        # 归１化与反归一解释
        val = m.predict(trains)
        divine = m.predict(turn_trains, batch_size=32, verbose=0)
        r = cr.alarm_divine(labels,divine,std)

        r = r.tolist()
        result = []
        for _data in r:
            _list = []
            for idx,d in enumerate(_data):
                nas = num_alarm_set[idx]
                if d <nas[0]:
                    _list.append(0)
                if nas[0] < d <nas[1]:
                    _list.append(1)
                if nas[1] <d:
                    _list.append(2)
            result.append(max(_list))
        # import pdb;pdb.set_trace()
        # result = np.array(result).transpose().tolist()
        for er in error_index:
            result[er]='2'
        self.write(dict(status=True, data=result,error_index=list(error_index)))
