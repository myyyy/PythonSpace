# -*- coding:utf-8 -*-
"""
    author comger@gmail.com
"""
import json
from kpages import service_async
from unittest import TestCase


from bson import ObjectId
import time
import numpy as np
import copy
import ast
import keras
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

class Mq(TestCase):
    
    def test_send(self):
        train_pid = os.getpid()
        code_name = 'nns_comger'
        MongoIns().m_update(T_MODEL, {'code_name':code_name},train_pid=train_pid)
        pkl_file = 'static/keras/{}.pkl'.format(code_name)
        yaml_file = 'static/keras/{}.h5'.format(code_name)
        try:
            os.remove(pkl_file)
            os.remove(yaml_file)
        except Exception as e:
            pass

        model = MongoIns().m_find_one(T_MODEL, code_name=code_name)
        lst, p = MongoIns().m_list(code_name+'_train', findall="1")
        data = []
        for f in (model.get('input')+model.get('output')):
            f_arr = []
            for node in lst:
                f_arr.append(node.get(f, None))
            data.append(f_arr)

        m = cr.get_model(code_name)
        data = np.asarray(data)
        data = data.transpose()
        trains = data[:, 0:len(model.get('input'))]
        labels = data[:, len(model.get('input')):]
        epochs = int(model.get('train_setting', {}).get('epochs', 10))
        batch_size = int(model.get('train_setting', {}).get('batch_size', 32))
        validation_split = float(model.get('train_setting', {}).get('validation_split', 0.1))

        #保存训练记录日志
        csv_file = 'static/keras/{}.csv'.format(code_name)
        csv_logger = keras.callbacks.CSVLogger(csv_file, separator=',', append=True)

        m.fit(trains, labels, nb_epoch=epochs, batch_size=batch_size,validation_split=validation_split,callbacks=[csv_logger])
        print '`````````````````',dir(resultfit),resultfit.history()
        score = m.evaluate(trains[2:12, :], labels[2:12, :], batch_size=batch_size)
        cr.create_plot(code_name, m)
        with open(csv_file, 'w+') as svgf:
            svgf.write('end tring')
        MongoIns().m_update(T_MODEL, {'code_name':code_name},train_pid=None)
