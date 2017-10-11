#!encoding=utf-8
import urllib 
import urllib2
import time
import json
from unittest import TestCase


import copy

import traceback
import time, json, math
import tornado.httpclient
from bson import ObjectId
from scipy import interpolate
from datetime import datetime, timedelta
from collections import defaultdict
from mongo_util import MongoIns

# from cache import Cache

def warningWholeMachine(data):
    _input = ['HomeWindSpeed', 'HimeGnSpeed', 'PitchPos1EncoderA']

    train_data = []
    for i in _input:
        train_data.append(data.get(i) or 0)

    args = {
                "code_name": 'nns_WindPower-01',
                "train_data": [train_data]
            }

    body = urllib.urlencode({'args': json.dumps(args)})
    http_client = tornado.httpclient.HTTPClient()
    req = tornado.httpclient.HTTPRequest("http://192.168.111.215:9995/evaluate/exec/api", method="POST", body=body)
    #req = tornado.httpclient.HTTPRequest("http://localhost:9995/evaluate/exec/api", method="POST", body = body)

    val = 0
    t1 = time.time()
    try:
        response = http_client.fetch(req)
        body = json.loads(response.body)
        val = body.get('data')[0][0]
    except Exception as e:
        traceback.print_exc()
        http_client.close()

    print '-' * 10, '整机评分:', 'mtrp----:',data.get('MtrP'), 'val-----:',val, train_data,data.get('_id')


def post(url, data): 
    post_data = urllib.urlencode(data)
    data = json.dumps(data)
    print data
    req = urllib2.urlopen(url, post_data)
    return req.read()
class Normalization(TestCase):

    # def test_get_mode(self):
    #     posturl = "http://192.168.111.215:9995/evaluate/exec/api"
    #     data = {}
    #     data['args'] = {
    #                     "code_name": "nns_WindPower-01",
    #                     "train_data": [
    #                         [9.4,   1483.2, 0.4]
    #                     ]
    #                 }

    #     t1 = time.time()
    #     for a in xrange(10000):
    #         t2 = time.time()
    #         rs = post(posturl, data) 
    #         print'!'*20, time.time()-t2,rs

    #     print time.time()-t1


    def test_get_mode(self):
        import pdb;pdb.set_trace()

        lt = 'fj_77_2017-06-29T23:30'
        gt = 'fj_77_2017-06-28T23:30'

        data,_ =MongoIns().m_list('data_m',dbname='wf_TieLing',_id={'$gte':gt,'$lte':lt},findall=True)
        for d in data:
            warningWholeMachine(d)






if __name__ == '__main__': 
  main() 