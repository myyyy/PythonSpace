# -*- coding:utf-8 -*-
"""
    author comger@gmail.com
    模型代码生成器
"""
import cPickle as pickle
import os
import time

import numpy as np
from tornado.template import Loader
from keras.models import model_from_json
from keras.models import load_model

from kpages import app_path,get_context
from mongo_util import MongoIns
from define_keras import LAYER,OPTIMIZER
from logic.define import *
from cache import Cache


LAYER_MAP = dict((layer.get('name'),layer) for layer in LAYER)
OPT_MAP = dict((layer.get('name'),layer) for layer in OPTIMIZER)


def get_model_data(code_name):
    model = MongoIns().m_find_one(T_MODEL,code_name=code_name)
    layers = []
    if model.get('struct_order',[]):
        for oid in model.get('struct_order',[]):
            for ly in model.get('struct',[]):
                if oid == ly['oid']:
                    layers.append(ly)
    else:
        layers = model.get('struct',[])    

    model['struct'] = layers
    return model


def render_parse(layers, optimizer={}, fix={}):
    for ly in layers:
        arr = []
        params = LAYER_MAP[ly['layer_name']].get('params')
        for p in params:
            val = ly.get('params',{}).get(p['name'],None)
            if not val and p['name'] not in ly.get('params',{}):
                continue

            dt = p.get('dt','str')
            if p.get('pt') ==1:
                if dt == 'str':
                    arr.append('"{}"'.format(val))
                else:
                    arr.append(val)
            else:
                print p['name'],val
                if val in ("None","True","False") or not val or type(val)==bool:
                    arr.append('{0}={1}'.format(p['name'],val))
                elif dt == 'str':
                    arr.append('{0}="{1}"'.format(p['name'],val))
                else:
                    arr.append('{0}={1}'.format(p['name'],val))

        pline = ''
        for item in arr:
            pline  +=  ','+ str(item)

        ly['pline'] = pline[1:]

    fix['mline'] = ''
    for m in fix.get('metrics',[]):
        fix['mline'] += ',"{}"'.format(m)
    fix['mline'] = fix['mline'][1:]

    if optimizer:
        ot = OPT_MAP[optimizer['optimizer']]
        arr = []
        for p in ot.get('params',[]):
            val = optimizer.get(p['name'],None)
            if not val and p['name'] not in ly.get('params',{}):
                continue

            dt = p.get('dt','str')
            if p.get('pt') ==1:
                if dt == 'str':
                    arr.append('"{}"'.format(val))
                else:
                    arr.append(val)
            else:
                print p['name'],val
                if val in ("None","True","False") or not val or type(val)==bool:
                    arr.append('{0}={1}'.format(p['name'],val))
                elif dt == 'str':
                    arr.append('{0}="{1}"'.format(p['name'],val))
                else:
                    arr.append('{0}={1}'.format(p['name'],val))

        pline = ''
        for item in arr:
            pline  +=  ','+ str(item)

        fix['oline'] = pline[1:]

        return layers, optimizer, fix

def code_render(layers, optimizer={}, fix={}):
    layers, optimizer, fix = render_parse(layers, optimizer=optimizer, fix=fix)

    loader = Loader(app_path('template'))
    code = loader.load('code.pyt').generate(layers=layers, optimizer=optimizer, fix=fix)
    return code


def create_model(layers, optimizer={}, fix={}):
    import keras
    from keras.models import Sequential
    from keras import optimizers
    
    code = code_render(layers,optimizer=optimizer,fix=fix) 
    print 'code-----------',code
    exec(code)
    return model




def create_plot(code_name,model):
    from keras.utils.vis_utils import plot_model

    h5_file = 'static/keras/{}.h5'.format(code_name)
    os.remove(h5_file)
    model.save(h5_file)
    if not os.path.exists('static/keras'):
        os.mkdir( 'static/keras' )
    plot_model(model, to_file='static/keras/{}.png'.format(code_name))

def get_model(code_name):

    pkl_file = 'static/keras/{}.pkl'.format(code_name)
    h5_file = 'static/keras/{}.h5'.format(code_name)

    cache_key = 'cache_model_{}'.format(code_name)

    if not os.path.exists(h5_file):
        model = get_model_data(code_name)
        m=  create_model(model.get('struct',()), optimizer=model.get('opt',{}), fix=model.get('fix',{}))
        m.save(h5_file)
        Cache().setex(cache_key, (m, time.time()), 60 * 10)
    else:
        cache_m = Cache().get(cache_key)

        if cache_m:
            m, ts = cache_m
            if ts < os.path.getmtime(h5_file):
                m = load_model(h5_file)
                Cache().setex(cache_key, (m, time.time()), 60 * 10)

        else:
            m = load_model(h5_file)
            Cache().setex(cache_key, (m, time.time()), 60 * 10)
    return m


def ai_render(code_name):
    md = get_model_data(code_name)
    epochs = int(md.get('train_setting', {}).get('epochs', 100))
    batch_size = int(md.get('train_setting', {}).get('batch_size', 32))
    validation_split = md.get('train_setting', {}).get('validation_split', 0.1)

    layers, optimizer, fix = render_parse(md.get('struct',()), optimizer=md.get('opt',{}), fix=md.get('fix',()))
    loader = Loader(app_path('template'))
    model = MongoIns().m_find_one(T_MODEL, code_name=code_name)
    train_min,train_deno = [], []
    evl_min, evl_deno = [], []
    std = model.get('output_std')
    for d in model.get('input'):
        train_min.append(model.get('num_set').get(d)[0])
        train_deno.append(model.get('num_set').get(d)[1]-model.get('num_set').get(d)[0])

    for d in model.get('output'):
        evl_min.append(model.get('num_set').get(d)[0])
        evl_deno.append(model.get('num_set').get(d)[1]-model.get('num_set').get(d)[0])

    code = loader.load('ai.pyt').generate(layers=layers, optimizer=optimizer, fix=fix,
                 input_num=len(md.get('input')),
                 output_num=len(md.get('output')),
                 nb_epoch=epochs,
                 batch_size=batch_size,
                 validation_split = validation_split,
                 code_name = code_name,
                 train_min = train_min,
                 train_deno = train_deno,
                 evl_min = evl_min,
                 evl_deno = evl_deno,
                 std = std
                 )

    return code



def normal(data):
    dmin,dmax = data.min(),data.max()
    if dmax > dmin:
        return (data-dmin)/(dmax-dmin)
    else:
        return np.asarray([0]*data.shape[0])


def normalization(data):
    data = map(lambda x:map(float,x),data.tolist())
    data = np.asarray(data)
    for i in range(data.shape[1]):
        data[:,i] = normal(data[:,i])

    return data

def normalization_new(data,minarray,denoarray):
    return (data-minarray)/denoarray

def turn_normalization(data,minarray,denoarray):
    return (data*denoarray)+minarray

def alarm_divine(realy,divine,std):
    return (divine-realy)/std

if __name__ == '__main__':
    layers = [{'name':'Dense', 'params':{
        'units':3,
        'input_dim':3,
        'activation':'softmax',

    }},{'name':'Activation', 'params':{
        'activation':'softmax'
    }}]
    print create_model(layers)
