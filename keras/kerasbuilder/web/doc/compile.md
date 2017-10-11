# 保存编译选项

```
    method:post,
    url:/compile/edit,
    ParameterChecking:{
        not None:code_name
    },
    RequestParam:{
        "code_name":"",
        (other args)
    },
    ReturnParam:
            {
                status: True,
                data: "添加成功"
            }

```

#　编译选项html

```
    method:get,
    url:/optimizer/html,
    ParameterChecking:{
        not None:optimizer,code_name
    },
    RequestParam:{
        "code_name":"",
        (other args)
    },
    ReturnParam:
            {
                status: True,
                data: html代码片段
            }
    data for html:
            {
                "default": {
                    "params": [
                        {
                            regex: "",
                            default: 0.01,
                            name: "lr",
                            comments: "float >= 0. Learning rate."
                        },
                        {
                            regex: "",
                            default: 1e-8,
                            name: "epsilon",
                            comments: "float >= 0. Fuzz factor."
                        },
                        {
                            regex: "",
                            default: 0,
                            name: "decay",
                            comments: "float >= 0. Learning rate decay over each update."
                        }
                    ],
                    name: "Adagrad",
                    module: "keras.optimizers.Adagrad",
                    comments: " It is recommended to leave the parameters of this optimizer at their default values. "
                },
                "status": true,
                "data": {
                    epsilon: 1e-8,
                    lr: 0.01,
                    optimizer: "Adagrad",
                    decay: 0
                }
            },

```

