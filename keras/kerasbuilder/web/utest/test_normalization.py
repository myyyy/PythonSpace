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
import random
import numpy as np

from logic.utility import BaseHandler
from logic.define import *
from logic.excel import *
from logic import code_render as cr
#kpages_tool.py --test test_normalization


class Normalization(TestCase):

    def test_normalization(self):
        # 归一化
        code = 'nns_nns_WindPower-FDJ'
        # trains = [[9.867857142857144, 1750.0, 1737.95, 1729.7250000000001, 31.175, 3.042857142857143, 1.3607142857142858]]
        # minarray = [0.021428571428571432, 1750.0, 0.0, 0.0, 12.5979923248291, 0.19101548196631485, 0.0]
        # maxarray = [22.803571428571427, 1751.0, 1784.3707264454422, 6552.5158813476555, 40.614285714285714, 20.73888888888889, 90.90000000000002]
        # denoarray =[22.782142857142855, 1, 1784.3707264454422, 6552.5158813476555, 28.016293389456614, 20.547873406922577, 90.90000000000002]
        # trains = np.array(trains)
        # minarray ,denoarray= np.array(minarray),np.array(denoarray)
        # nordata = cr.normalization_new(trains, minarray,denoarray)
        # turn_trains = cr.turn_normalization(nordata,minarray,denoarray)
        # print '###'*10
        # print 'nordata---',nordata.tolist()
        # print 'denoarray',denoarray.tolist()
        # print 'minarray',minarray.tolist()
        
        # print 'trains------',trains.tolist()
        # print 'turn_trains',turn_trains.tolist()

    def test_keras_model(self):
        code_name = 'nns_WindPower-01'
        # trains = [[random.uniform(0, 1)  for i in range(6)],]
        # m = cr.get_model(code_name)
        # result = m.predict(np.array(trains))
        # print 'result***',result
        # print 'trains***',trains
        data = [[7.11236907691,  1378.73322895,0.0]]
        model = MongoIns().m_find_one(T_MODEL, code_name=code_name)
        num_set = model.get('num_set')
        minarray = []
        denoarray =[]
        for k in model.get('input',[]):
            _min = num_set.get(k)[0]
            _max = num_set.get(k)[1]
            minarray.append(_min)
            denoarray.append(1 if (_max-_min)==0 else (_max-_min))
        trains = cr.normalization_new(np.array(data),np.array(minarray),np.array(denoarray))
        m = cr.get_model(code_name)
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
        print turn_result