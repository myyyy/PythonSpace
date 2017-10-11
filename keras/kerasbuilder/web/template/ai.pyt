# -*- coding:utf-8 -*-
"""
    author comger@gmail.com
"""
import csv
import numpy as np
import keras
from keras.models import Sequential
from keras import optimizers

train_min= {{train_min}}
train_deno = {{train_deno}}
evl_min = {{evl_min}}
evl_deno = {{evl_deno}}
std = {{std}}

def normalization_new(data,minarray,denoarray):
    return (data-minarray)/denoarray

def turn_normalization(data,minarray,denoarray):
    return (data*denoarray)+minarray

def alarm_divine(realy,divine,std):
    return (divine-realy)/std

##############
def normal(data):
    dmin,dmax = data.min(),data.max()
    if dmax > dmin:
        return (data-dmin)/(dmax-dmin)
    else:
        return np.asarray([0]*data.shape[0])


def normalization(data):
    for i in range(data.shape[1]):
        data[:,i] = normal(data[:,i])

    return data

def get_data(dtype,input_num, output_num):

    train = []
    train_label = []
    check = []
    with open(dtype+'-{{code_name}}.csv') as f:
        reader = csv.reader(f)
        for line in reader:
            line = map(float,line)
            if line:
                train.append(line[0:input_num])
                train_label.append(line[input_num:(input_num+output_num)])
    t,l = np.asarray(train),np.asarray(train_label)
    t = normalization_new(t,np.array(train_min),np.array(train_deno))
    l = normalization_new(l,np.array(evl_min),np.array(evl_deno))
    return t, l


model = Sequential()
{% for ly in layers %}model.add(keras.layers.core.{{ly['layer_name']}}({% raw ly['pline']%}))
{% end %}{% if optimizer%}
v_opt = optimizers.{{optimizer.get('optimizer')}}({% raw fix['oline']%})
model.compile(optimizer=v_opt,loss='{{ fix.get('loss','categorical_crossentropy')}}', metrics=[{% raw fix['mline'] %}])
{% else %}
model.compile(optimizer="rmsprop",loss='{{ fix.get('loss','categorical_crossentropy')}}', metrics=[{% raw fix['mline'] %}])
{% end %}

# 模型训练
trains, labels = get_data('train',{{input_num}},{{output_num}})

model.fit(trains, labels, nb_epoch={{nb_epoch}}, batch_size={{batch_size}},validation_split={{validation_split}},verbose=1)

#模型预测
trains, labels = get_data('evaluate',{{input_num}},{{output_num}})
print '预测结果为:',model.evaluate(trains, labels, batch_size={{batch_size}})
