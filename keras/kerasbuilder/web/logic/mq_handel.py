# -*- coding:utf-8 -*-
import numpy as np
import psutil
import os

from kpages import srvcmd,get_context
from os import fork
from mongo_util import MongoIns
from logic.define import T_MODEL
from logic import code_render as cr
import keras

@srvcmd('mq_train')
def mq_train(data):
    '''训练消息队列'''
    # train_status 为0表示训练终止，１表示训练开始或者在训练中
    print 'xxxxx'
    try:
        forkid=os.fork()
        if forkid>0:
            return
        train_pid = os.getpid()
        code_name = data.get('code_name','')
        MongoIns().m_update(T_MODEL, {'code_name':code_name},train_pid=train_pid,train_status='1')
        csv_file = 'static/keras/{}.csv'.format(code_name)
        h5_file = 'static/keras/{}.h5'.format(code_name)
        try:
            os.remove(csv_file)
            os.remove(h5_file)
            print '删除．．．．．mq'
        except Exception as e:
            pass

        model = MongoIns().m_find_one(T_MODEL, code_name=code_name)
        lst, p = MongoIns().m_list(code_name+'_train', findall="1")
        num_set = model.get('num_set')
        data = []
        minarray = []
        denoarray =[]
        for f in (model.get('input')+model.get('output')):
            f_arr = []
            for node in lst:
                f_arr.append(float(node.get(f, None)))
            data.append(f_arr)
            #获取设置中最大最小值
            _min = num_set.get(f)[0]
            _max = num_set.get(f)[1]
            minarray.append(_min)
            denoarray.append(1 if (_max-_min)==0 else (_max-_min))


        print 'get_model．．．．．mq'
        m = cr.get_model(code_name)
        data = np.asarray(data)
        data = data.transpose()
        #反归一化之前的标准差
        output_std = np.std(data[:, len(model.get('input')):], axis=0).tolist()
        output_std = map(lambda x: 1 if x==0 else x,output_std)
        MongoIns().m_update(T_MODEL, {'code_name':code_name},output_std=output_std)
        # 归一化
        data = cr.normalization_new(data,np.array(minarray),np.array(denoarray))
        trains = data[:, 0:len(model.get('input'))]
        labels = data[:, len(model.get('input')):]
        epochs = int(model.get('train_setting', {}).get('epochs', 10))
        batch_size = int(model.get('train_setting', {}).get('batch_size', 32))
        validation_split = float(model.get('train_setting', {}).get('validation_split', 0.1))
        #保存训练记录日志
        csv_logger = keras.callbacks.CSVLogger(csv_file, separator=',', append=False)

        m.fit(trains, labels, nb_epoch=epochs, batch_size=batch_size,validation_split=validation_split,callbacks=[csv_logger],verbose=1)
        cr.create_plot(code_name, m)
        with open(csv_file, 'a') as svgf:
            svgf.write('end traing')
        MongoIns().m_update(T_MODEL, {'code_name':code_name},train_status='0')

        p = psutil.Process(train_pid)
        p.kill()

    except Exception as e:
        import traceback
        traceback.print_exc()

        train_pid = os.getpid()
        p = psutil.Process(train_pid)
        p.kill()
        MongoIns().m_update(T_MODEL, {'code_name':code_name},train_status='0',error=traceback.format_exc())


def test():
    print '123'


def  mq_test(data):
    if fork()>0:
        print '------'
        return

    forkid= os.getpid()
    print '------',data,forkid



import os  
  
def child():  
    print 'A new child:', os.getpid()  
    print 'Parent id is:', os.getppid()  
    os._exit(0)  

@srvcmd('mq_test')
def parent():  

    newpid=os.fork()  
    print newpid  
    if newpid==0:  
        child()  
    else:  
        pids=(os.getpid(),newpid)  
        print "parent:%d,child:%d"%pids  
        print "parent parent:",os.getppid()         
