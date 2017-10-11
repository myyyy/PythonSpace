#!encoding=utf-8
from define_keras import *

T_MODEL = 'model'
LAYEAR_STATUS = 'layear_status'
TRAIN_DATA = "train_data"
LAYER_MAP = dict((layer.get('name'),[layer.get('module'),layer.get('comments')]) for layer in LAYER)

OPTIMIZER_MAP = dict((opt.get('name'),[opt.get('module'),opt.get('comments')]) for opt in OPTIMIZER)
