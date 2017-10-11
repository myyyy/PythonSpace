# 获取单个模型

```
    method:get,
    url:/model/data,
    ParameterChecking:{
        not None:code_name
    },
    RequestParam:{
        "name":"",
    },
    ReturnParam:{
              "status": True,
              "data": model_data
            }

```


#　添加模型（input,output不能有相同的名称）

```
    method:post,
    url:/model/add,
    ParameterChecking:{
        not None:code_name,name
    },
    RequestParam:{
        "name":"",
        "code_name":"",
        "input":"i1,i2,i3",
        "output":"o1,o2,o3",
    },
    ReturnParam:{
              "status": True,
              "data": ""
            }

```

#　编辑模型 （input,output不能有相同的名称）

```
    method:post,
    url:/model/edit,
    ParameterChecking:{
        not None:code_name,name
    },
    RequestParam:{
        "name":"",
        "code_name":"",
        "input":"i1,i2,i3",
        "output":"o1,o2,o3",
    },
    ReturnParam:{
              "status": True,
              "data": ""
            }
```

#　下載aipy文件

```
    method:get,
    url:/model/download/aipy,
    ParameterChecking:{
        not None:code_name
    },
    ReturnParam:file
```

#　删除模型

```
    method:post,
    url:/model/del,
    ParameterChecking:{
        not None:code_name
    },
    RequestParam:{
        "code_name":"",
    },
    ReturnParam:{
              "status": True,
              "data": ""
            }
```
#　主页面侧边栏　模型　由后端渲染

```
    method:get,
    url:/,
    ParameterChecking:{
        not None:
    },
    RequestParam:{
    },
    ReturnParam:html,
    data for html:
            [
                {
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
                },
                
            ]
```

(status,list(item)):post:url{
    abc:xxd,int,xxx,
},


#　删除模型

```
    method:post,
    url:/model/del,
    ParameterChecking:{
        not None:code_name
    },
    RequestParam:{
        "code_name":"",
    },
    ReturnParam:{
              "status": True,
              "data": ""
            }
```