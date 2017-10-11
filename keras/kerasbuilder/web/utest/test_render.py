# -*- coding:utf-8 -*-
"""
    author cmger@gmail.com
"""
from unittest import TestCase
from logic.code_render import code_render,create_model


class RenderCase(TestCase):
    def setUp(self):
        pass
        

    def test_print(self):
        layers = [{'name':'Dense', 'params':{
            'input_dim':3,
            'kernel_regularizer':None,
            'activation':'softmax',

        }},{'name':'Activation', 'params':{
            'activation':'softmax'
        }}]
        print code_render(layers)
        #print create_model(layers)






