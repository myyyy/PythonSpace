#　添加结构

```
    method:post,
    url:/layer/add,
    ParameterChecking:{
        not None:code_name,layer_name
    },
    RequestParam:{
        "code_name":"",
        "layer_type":"",
        (other args->key:value)
    },
    ReturnParam:{
              "status": True,
              "data": ""
            }
```

#　编辑结构

```
    method:post,
    url:/model/edit,
    ParameterChecking:{
        not None:code_name,layer_type,oid
    },
    RequestParam:{
        "code_name":"",
        "layer_type":"",
        "oid":"",
        (other args)
    },
    ReturnParam:{
              "status": True,
              "data": ""
            }
```



#　删除结构

```
    method:post,
    url:/model/del,
    ParameterChecking:{
        not None:code_name,oid
    },
    RequestParam:{
        "code_name":"",
        "oid":""
    },
    ReturnParam:{
              "status": True,
              "data": ""
            }
```

#　结构排序

```
    method:post,
    url:/model/edit/order,
    ParameterChecking:{
        not None:code_name,struct_order
    },
    RequestParam:{
        "code_name":"",
        "struct_order":"oid,oid,oid"
    },
    ReturnParam:{
              "status": True,
              "data": ""
            }
```

#　结构列表页面

```
    method:get,
    url:/struct/list/html,
    ParameterChecking:{
        not None:code_name
    },
    RequestParam:{
        "code_name":"",
        "struct_order":"oid,oid,oid"
    },
    ReturnParam:
            {
                status: True,
                data: html代码片段,
                code: "",
                imgurl: "static/nns_char.png"
            },
    data for html:
                {
                        "data":{
                            opt: {
                                epsilon: 1e-8,
                                lr: 0.01,
                                optimizer: "Adagrad",
                                decay: 0
                            },
                            struct_order: [
                                "5924f36c35f9a875cfa1908d",
                                "59251baaa5d158000b0c1e55"
                            ],
                            code: "model.add(Dense(1,use_bias=True,kernel_initializer="glorot_uniform",bias_initializer="zeros")) model.add(Masking()) ",
                            name: "char",
                            code_name: "nns_char",
                            input: [
                                "输入1",
                                "输入2",
                                "输入3"
                            ],
                            output: [
                                "输出1",
                                "输出2",
                                "输出3"
                            ],
                            _id: "591e671a35f9a810b7431f6c",
                            struct: [
                                {
                                    oid: "5924f36c35f9a875cfa1908d",
                                    params: {
                                        units: 1,
                                        use_bias: "True",
                                        kernel_initializer: "glorot_uniform",
                                        bias_initializer: "zeros"
                                    },
                                    layer_name: "Dense"
                                },
                                {
                                    oid: "59251baaa5d158000b0c1e55",
                                    params: {
                                        
                                    },
                                    layer_name: "Masking"
                                }
                            ]
                        }



                }

```
# 结构｜代码块

```
    method:get,
    url:/layer/codeblock,
    ParameterChecking:{
        not None:code_name
    },
    RequestParam:{
        "code_name":"",
    },
    ReturnParam:
            {
                status: True,
                data: "model.add(Dense(1,use_bias=True,kernel_initializer="glorot_uniform",bias_initializer="zeros")) "
            }

```


# 结构｜代码块同步

```
    method:get,
    url:/layer/codeblock/synchro,
    ParameterChecking:{
        not None:code_name
    },
    RequestParam:{
        "code_name":"",
    },
    ReturnParam:
            {
                status: True,
                data: "model.add(Dense(1,use_bias=True,kernel_initializer="glorot_uniform",bias_initializer="zeros")) "
            }

```

# 结构｜代码块图片预览同步

```
    method:get,
    url:/layer/codeview,
    ParameterChecking:{
        not None:code_name
    },
    RequestParam:{
        "code_name":"",
    },
    ReturnParam:
            {
                status: True,
                data: url
            }

```

# 下载结构

* 只支持全部导出

```
    method:get,
    url:/layer/download,
    ParameterChecking:{
        not None:code_name
    },
    RequestParam:{
        "code_name":"",
    },
    ReturnParam:file  (filename:模型名称-模型结构.json)

```


# 上传结构


```
    method:post,
    url:/layer/upload,
    ParameterChecking:{
        not None:code_name
    },
    RequestParam:{
        "uploadfile":file,
    },
    ReturnParam:
            {
                status: True,
                data: "添加成功"
            }

```

# ps

｀｀｀
下载结构中数据文件格式同上传结构数据文件格式

[
    {
        "params": {
            "rate": null, 
            "noise_shape": null, 
            "seed": null
        }, 
        "layer_name": "Dropout"
    }, 
    {
        "params": {}, 
        "layer_name": "Reshape"
    }
]

｀｀｀