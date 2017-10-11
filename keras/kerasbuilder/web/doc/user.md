
# 添加用户

* 计划后天用脚本添加一个用户

# 用户登录

```
    method:post,
    url:/login,
    ParameterChecking:{
        not None:username,password
    },
    RequestParam:{
        "username":"",
        "password":"",
    },
    ReturnParam:{
              "status": True,
              "data": "登录成功"
            }

```
# 用户注销

```
    method:get,
    url:/logout,

```

# 单个用户查看

```
    method:get,
    url:/user,
    ParameterChecking:{
        not None:username
    },
    RequestParam:{
        "username":"",
    },
    ReturnParam:{
              "status": True,
              "data": {
                    "username":"",
                    "password":"",
                    "email":"",
                }
            }

```


# 单个用户编辑

```
    method:post,
    url:/user/edit,
    ParameterChecking:{
        not None:username,password
    },
    RequestParam:{
        "username":"",
        "password":"",
    },
    ReturnParam:{
              "status": True,
              "data": "修改成功"
            }

```
＃ 用户管理？

