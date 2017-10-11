#获取所有模型信息
> GET
> URL:http://127.0.0.1:9995/model/data/all

#获取所有单个模型信息
> GET
> URL:http://127.0.0.1:9995/model/data?code_name=Alpha

#编辑模型
> POST
> http://127.0.0.1:9995/model/edit?code_name=xxx&layer_type&params&activation

#添加模型
> POST
> http://127.0.0.1:9995/model/add?name=Alpha&code_name=nns_alpha

#删除模型
> POST
> http://127.0.0.1:9995/model/del?code_name=xxx

<!-- #编译 编辑
> POST
> http://127.0.0.1:9995/compile/edit?code_name=xxx(args:code_name,Optimizer,lr,momentum,decay,nesterov,loss,metrics)
#获取 optimizer
> GET
> http://127.0.0.1:9995/optimizer
 -->

#获取layers
> GET
> http://127.0.0.1:9995/layer/html?code_name=char&oid=5922887035f9a853f8b1557f&layer_name=xxx

# 添加结构
> POST
> http://127.0.0.1:9995/layer/add?layer_name=Dense&code_name=char&units=1.0&activation=2.0

# 编辑结构
> POST
> http://127.0.0.1:9995/layer/edit

# 删除结构
> POST
> http://127.0.0.1:9995/layer/del?code_name=char&oid=5922786d35f9a846d81a38b3
# 获取模型全部结构 
> http://127.0.0.1:9995/model/data/all
# 结构排序
>ＰＯＳＴ
＞　127.0.0.1:9995/layer/edit/order?struct_order=59240d0f35f9a849814e2c83,59240d0735f9a849814e2c82 &code_name=nns_DVA

# 同步代码块
> GET
> http://127.0.0.1:9995/layer/codeblock/synchro?code_name=nns_char
# 获取代码块
> GET
> http://127.0.0.1:9995/layer/codeblock?code_name=nns_char

#獲取编译选项html
> GET
> http://127.0.0.1:9995/optimizer/html?optimizer=SGD

#编辑添加编译选项html
> GET
> http://127.0.0.1:9995/compile/edit?optimizer=1&lr=23&momentum=1&decay=1&nesterov=2&code_name=char

# 模型下载
> 127.0.0.1:9995/layer/download?code_name=char

# 模型导入
>http://127.0.0.1:9995/layer/upload
> 模板
    {
            "params" : {
                "kernel_initializer" : "  glorot_uniform ",
                "bias_regularizer" : "  None ",
                "kernel_constraint" : "  None ",
                "bias_constraint" : "  None ",
                "activation" : "  None ",
                "kernel_regularizer" : "  None ",
                "bias_initializer" : "  zeros ",
                "units" : "   ",
                "use_bias" : "  True ",
                "activity_regularizer" : "  None "
            },
            "layer_name" : "ssssss"
    }

# 训练数据列表
>GET
> http://127.0.0.1:9995/train/list/html?code_name=nns_char&handle_type=train

# 训练数据excel导入
> POST
> http://127.0.0.1:9995/train/excel/upload?code_name=nns_char&is_del_history=True&uploadfile=file&handle_type=train('train' or 'evaluate')(若勾选历史数据则is_del_history=True 否则为False)
# 训练数据excel导出
> get
> http://127.0.0.1:9995/train/excel/download?code_name=nns_char&handle_type=train

# 同　训练数据　evaluae　ｒｅｐｌａｃｅ　ｔｒａｉｎ

