```
    {
        "_id" : ObjectId("59240d0035f9a849814e2c81"),
        "output" : [ 
            "DV"
        ],
        "name" : "DVA(勿删)",
        "code_name" : "nns_DVA",
        "input" : [ 
            "DVA"
        ],
        "struct_order" : [ 
            "59240d0f35f9a849814e2c83", 
            "59240d0735f9a849814e2c82", 
            "59241062a5d158000b49e27c"
        ],
        "struct" : [ 
            {
                "oid" : "59240d0735f9a849814e2c82",
                "params" : {
                    "target_shape" : ""
                },
                "layer_name" : "Reshape"
            }, 
            {
                "oid" : "59240d0f35f9a849814e2c83",
                "params" : {
                    "rate" : null,
                    "noise_shape" : null,
                    "seed" : null
                },
                "layer_name" : "Dropout"
            }, 
            {
                "oid" : "59241062a5d158000b49e27c",
                "params" : {
                    "rate" : "223",
                    "noise_shape" : "No",
                    "seed" : null
                },
                "layer_name" : "Dropout"
            }
        ],
        "opt" : {
            "beta_1" : 0.9,
            "beta_2" : 0.999,
            "optimizer" : "Nadam",
            "epsilon" : 1e-08,
            "lr" : 0.002,
            "schedule_decay" : 0.004
        },
        "code" : "model.add(Dropout(rate=None,noise_shape=None,seed=None))\nmodel.add(Reshape(target_shape=))\nmodel.add(Dropout(rate=223,noise_shape=\"No\",seed=None))\n",
        "train_setting" : {
            "xxx" : "xx,xx "
        },
        "evaluate_setting" : {
            "xxx" : "xxx"
        },
        "train_mongo_seeting" : {
        "username" : "",
        "is_del_history" : "",
        "database" : "",
        "export" : "",
        "sql" : "",
        "password" : ""
    }
    }
```