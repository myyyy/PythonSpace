?　支持不支持添加单个
#　训练数据编辑

```
* 数据编辑
    method:post,
    url:/train/edit,
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
              "data": "编辑成功"
            }

* 获得指定条训练数据
    method:get,
    url:/train/edit,
    ParameterChecking:{
        not None:_id,code_name
    },
    RequestParam:{
        "code_name":"",
        "_id":"id",
    },
    ReturnParam:
            {
                status: true,
                data: {
                    DVA1: 3,
                    DVA2: 2,
                    _id: "592404e635f9a840c4bd9d07"
                },
                title: [
                "DVA1",
                "DVA2"
                ]
            }

```

#　训练数据删除(支持批量删除)


```
    method:post,
    url:/train/edit,
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


#　训练数据导入

```
    method:post,
    url:/train/excel/upload,
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

#　训练数据下载

```
    method:post,
    url:/train/excel/upload,
    ParameterChecking:{
        not None:code_name
    RequestParam:{
        "code_name":"",
    },
    ReturnParam:file

```


#　训练数据Mongo导入
* post:127.0.0.1:9995/train/mongo/upload?code_name=nns_DVA&url=192.168.111.147:27017/nns/model&sql={}&export=1,2&is_del_history=no

```
    method:post,
    url:/train/mongo/upload,
    ParameterChecking:{
        not None:code_name,sql,export,is_del_history
    RequestParam:{
        "code_name":"",
        "sql":"",
        "url":"",
        "export":"f1,f2,f3",
        "is_del_history":true or false,
    },
    ReturnParam:{
                status: True,
                data: "导入成功"
            }

```

#　训练设置　获得数据
```
    method:get,
    url:/model/data,
    ParameterChecking:{
        not None:code_name
    RequestParam:{
        "code_name":"",
    },
    ReturnParam:{
                status: True,
                data: {}
            }
获取data中　train_setting 数据
```

#　训练设置　训练
```
    method:post,
    url:/train/setting/edit,
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

#　开始训练
```
    method:post,
    url:/train/exec,
    ParameterChecking:{
        not None:code_name
    ReturnParam:{
                status: True,
                data: "训练指令发送成功"
            }

```
#　终止训练
```
    method:get,
    url:/train/exec,
    ParameterChecking:{
        not None:code_name
    ReturnParam:{
                status: True,
                data: "训练指令发送成功"
            }

根据/model/data　这个借口获取到train_status为＇１＇则终止按钮可以点击

```



#　模型训练 后台日志信息输出
```
    method:get,
    url:/train/exec/log,
    ParameterChecking:{
        not None:code_name
    ReturnParam:{
                status: True,
                data:  [
                    "epoch,loss,val_loss ",
                    "0,nan,nan ",
                    "1,nan,nan ",
                    "2,nan,nan ",
                    "3,nan,nan ",
                    "4,nan,nan ",
                    "5,nan,nan ",
                    "6,nan,nan ",
                    "7,nan,nan ",
                    "8,nan,nan ",
                    "9,nan,nan "
                    ]
            }

```