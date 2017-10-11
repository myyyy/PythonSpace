#　模型评测编辑

```
    method:post,
    url:/evaluate/edit,
    ParameterChecking:{
        not None:_id,code_name
    },
    RequestParam:{
        "code_name":"",
        "_id":"id",
        (other args)
    },
    ReturnParam:{
              "status": True,
              data: "编辑成功"
            }

```

#　模型评测删除

```
    method:post,
    url:/evaluate/edit,
    ParameterChecking:{
        not None:_id,code_name
    },
    RequestParam:{
        "code_name":"",
        "_id":"i1,i2,i3",
    },
    ReturnParam:{
              "status": True,
              data: "删除成功"
            }

```


#　模型评测导入

```
    method:post,
    url:/evaluate/excel/upload,
    ParameterChecking:{
        not None:code_name,is_del_history
    },
    RequestParam:{
        "code_name":"",
        "is_del_history":true or false
    },
    ReturnParam:{
              "status": True,
              "data": ""
              "uploadfile":file
            }

```

#　模型评测下载

```
    method:post,
    url:/evaluate/excel/upload,
    ParameterChecking:{
        not None:code_name
    RequestParam:{
        "code_name":"",
    },
    ReturnParam:file

```


#　模型评测Mongo导入

```
    method:post,
    url:/evaluate/mongo/upload,
    ParameterChecking:{
        not None:url,sql,export,is_del_history
    RequestParam:{
        "code_name":"",
        "sql":"",
        "export":"f1,f2,f3",
        "is_del_history":true or false
    },
    ReturnParam:{
                status: True,
                data: "导入成功"
            }

```

#　模型评测设置　获得数据
```
    method:get,
    url:/evaluate/setting,
    ParameterChecking:{
        not None:code_name
    RequestParam:{
        "code_name":"",
    },
    ReturnParam:{
                status: True,
                data: {
                    "batch_size":100,
                    "epochs":0.1,
                    "validation_split":0.1,
                    "shuffle":true
                }
            }

```
<!-- 
#　模型评测设置　编辑
```
    method:post,
    url:/evaluate/setting/edit,
    ParameterChecking:{
        not None:code_name
    RequestParam:{
        "code_name":"",
        "batch_size":100,
        "epochs":0.1,
        "validation_split":0.1,
        "shuffle":true
    },
    ReturnParam:{
                status: True,
                data: "编辑成功"
            }
 -->
```
#　模型评测 api

```
    method:post,
    url:/evaluate/setting/edit,
    ParameterChecking:{
        not None:args
        }
    RequestParam:{
        "args":{
                "code_name": "nns_comger",
                "batch_size": 32,
                "verbose": 0,
                "train": [
                    [
                        0,
                        0,
                        0
                    ],
                    [
                        0.30000000000000004,
                        0,
                        0.30000000000000004
                    ],
                    [
                        0.67,
                        0,
                        0.67
                    ]
                ]
            },
    },
    ReturnParam:
                    {
                        "status": true,
                        "data": [
                        [
                          0,
                          0
                        ],
                        [
                          -0.13028261065483093,
                          -0.21622085571289062
                        ],
                        [
                          -0.26174381375312805,
                          -0.41835781931877136
                        ]
                        ]
                    }

```

#　模型评测ＡＰＩ

```
    method:post,
    url:/evaluate/exec/api,
    ParameterChecking:{
        not None:args
    RequestParam:{
        "args":{
                "code_name": "nns_comger",
                "train_data": [
                    [0,0,0],
                    [0.30000000000000004,0,0.30000000000000004],
                    [
                        0.67,
                        0,
                        0.67
                    ]
                ]
            }
    },
    ReturnParam:{
                  "status": true,
                  "data": [
                    [
                      0,
                      0
                    ],
                    [
                      -0.10715864598751068,
                      0.15751489996910095
                    ],
                    [
                      -0.19340775907039642,
                      0.3223046660423279
                    ]
                  ]
            }

```

#　模型评测得分ＡＰＩ

```
    method:post,
    url:/evaluate/exec/score/api,
    ParameterChecking:{
        not None:args
    RequestParam:{
        "args":{
                "code_name": "nns_comger",
                "train_data": [
                    [0,0,0],
                    [0.30000000000000004,0,0.30000000000000004],
                    [
                        0.67,
                        0,
                        0.67
                    ]
                ]，
                "label_data": [
                    [0,0,0],
                    [0.30000000000000004,0,0.30000000000000004],
                    [
                        0.67,
                        0,
                        0.67
                    ]
                ]
            }
    },
    ReturnParam:{
                  "status": true,
                  "data": [
                    [
                      0,
                      0
                    ],
                    [
                      -0.10715864598751068,
                      0.15751489996910095
                    ],
                    [
                      -0.19340775907039642,
                      0.3223046660423279
                    ]
                  ]
            }

```