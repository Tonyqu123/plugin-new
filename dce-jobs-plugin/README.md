# 应用作业平台

## 分支
```
master
develop
    - backend
    - frontend

```

## DCS 项目
```
dce-jobs-plugin: https://dashboard.daocloud.io/orgs/daocloud/build-flows/3af948dd-48a4-4d18-94ba-cbe8a9033fe3
```

## API

### error handler
```
状态码:
    - 400
    - 404
    - 500
response:
    400 or 404:
        id 代表什么类型错误, 判断什么问题
        message 可能是一句话或者是出错的 objectId, 具体看每个 api 下面
        {
            "message": "job_id_not_found",
            "id": "job_id_not_found"
        }
    500:
        go find api owner
```

### 获取 jobs
```
GET /api/jobs
param:
    - AppName: 可选 过滤 AppName
response:
    注意, SecretArgs 返回的是 ***, 表示每个参数的长度.
    response 中的 SecretArgs 只会有 ["*", "**"], 直接展示在输入框就好, 空格分开
    [
        {
            "JobId": "{ uuid }",
            "AppName": "2048",
            "ServiceName": "2048_2048",
            "Name": "上线",
            "Cmd": "ps axu",
            "Privileged": true,
            "User": "root:root",
            "Env": ["a=b", "c=d"]
            "SecretArgs": ["*", "**"]
            "Executors": [
                ExecutorId1, ExecutorId2, ……
            ]
        },
        ......
        ......
    ]
command:

```

### 创建 jobs
```
POST /api/jobs
data:
    只有这里的 SecretArgs 是明文传输
    {
        "AppName": "2048",
        "ServiceName": "2048_2048",
        "Name": "上线",
        "Cmd": "ps axu",
        "Privileged": true,
        "User": "root:root",
        "Env": ["a=b", "c=d"]
        "SecretArgs": ["xxx", "yyy"]
    }
response:
200
    {
        "JobId": "{ uuid }"
        "AppName": "2048",
        "ServiceName": "2048_2048",
        "Name": "上线",
        "Cmd": "ps axu",
        "Privileged": true,
        "User": "root:root",
        "Env": ["a=b", "c=d"]
        "SecretArgs": ["*", "**"]
        "Executors": [
            ExecutorId1, ExecutorId2, ......
        ]
    }
400
    jobs_name_duplicated_error
        - { name } # 作业名称重复
```

### 编辑作业
```
PUT /api/jobs/{ uuid }
data:
    注意, 如果没修改, SecretArgs 就把获取到的 ["*", "**"] 上传上来
    {
        "AppName": "2048",
        "ServiceName": "2048_2048",
        "Name": "上线",
        "Cmd": "ps axu",
        "Privileged": true,
        "User": "root:root",
        "Env": ["a=b", "c=d"]
        "SecretArgs": ["*", "**"]
    }
response:
200
    {
        "JobId": "{ uuid }"
        "AppName": "2048",
        "ServiceName": "2048_2048",
        "Name": "上线",
        "Cmd": "ps axu",
        "Privileged": true,
        "User": "root:root",
        "Env": ["a=b", "c=d"]
        "SecretArgs": ["*", "**"]
        "Executors": [
            ExecutorId1, ExecutorId2, ......
        ]
    }
404
    job_id_not_found
        - { jobId } # 作业 ID 未找到
```

### 删除作业
```
DELETE /api/jobs/{ jobID }
response:
202
404
    job_id_not_found
        - { jobId } # 作业 ID 未找到
```

### 启动执行作业
```
POST /api/jobs/{ jobID }/start
data:
    {
        "Target": [
            {"ContainerId": "xxx", "NodeId": "yyy"},
            {"ContainerId": "aaa", "NodeId": "bbb"}
        ......
        ]
    }
response:
200
    请求结束, "Executors" 中的最后一个 `ExecutorId3` (timestamp) 代表新建的 Executor
    {
        "JobId": "{ uuid }"
        "AppName": "2048",
        "ServiceName": "2048_2048",
        "Name": "上线",
        "Cmd": "ps axu",
        "Privileged": true,
        "User": "root:root",
        "Env": ["a=b", "c=d"]
        "SecretArgs": ["*", "**"]
        "Executors": [
            ExecutorId1, ExecutorId2,  ExecutorId3......
        ]
    }
404
    job_id_not_found
        - { jobId } # 作业 ID 未找到
```

### 查看作业上一次的结果
```
GET /api/jobs/{ jobID }/inspect/{ timestamp }
timestamp 也就是 ExecutorId3
response:
200

    if status in [STARTING, CREATED]:
        执行中
    elif status in [CREATE_FAILED, RUNNING_FAILED]:
        失败
        详情显示 E
    elif status in [RUNNING]:
        执行中
    elif status in [FINISHED]:
        if ExitCode == 0:
            成功
            详情显示 Output
        else:
            失败
            详情显示 Output



    Status:
        - STARTING
        - CREATED
        - CREATE_FAILED    失败
        - RUNNING          执行中
        - RUNNING_FAILED   失败
        - FINISHED         

    如下, inspect 某个 executor 的结果
    response 中的 {{.Target}} 可能会被弃用, 因为和 {{.Result}} 中的数据是一样的顺序
    主要看 Result.
    Result[0:2] 前两个是执行完成, 查看 {{.ExitCode}} 来是成功 or 失败
        - 有多个属性
        - ExitCode -> 0 成功 其他失败
        - Output 是作业执行的输出
    Result[2:5] 后三个是执行中
        - 只有 NodeId / ContainerId / ID 三个属性

    {
        "JobId": "{ uuid }",
        "CreateTime": 1496287694.460088,
        "Target": [
            {
                "ContainerId": "a6c71c6f032a49487bc49d51d4de6d763a44e59addfc4a1c1b161a0728499f66",
                "NodeId": "guv4tovwx67oa4j9evjrcgg5v"
            },
            {
                "ContainerId": "ece76b382bc599702e2a451d627bd83f77ce1faf1a93e867574688ba46cf5112",
                "NodeId": "wn99oc5gv7u0ugt7yih5ymdw4"
            },
            {
                "ContainerId": "c2ed986a541c8336f8f2c88230de1a53bfd0c8d6929d2c7bda09185cbf3c8c5c",
                "NodeId": "wn99oc5gv7u0ugt7yih5ymdw4"
            },
            {
                "ContainerId": "4b9f9b3978f13324782beeadb2c7d612287d2b0ad1daea1d700e00352c1ba011",
                "NodeId": "wn99oc5gv7u0ugt7yih5ymdw4"
            },
            {
                "ContainerId": "10fead3fd22f4e43b91019a642081b5759dd1bff25c23e5ddceb67164979e41a",
                "NodeId": "guv4tovwx67oa4j9evjrcgg5v"
            }
        ]
        "Result": [
            {
                "Status": ""
                "OpenStderr": true,
                "OpenStdout": true,
                "ContainerId": "a6c71c6f032a49487bc49d51d4de6d763a44e59addfc4a1c1b161a0728499f66",
                "DetachKeys": "",
                "ExitCode": 0,
                "Pid": 27396,
                "NodeId": "guv4tovwx67oa4j9evjrcgg5v",
                "CanRemove": false,
                "Running": false,
                "ProcessConfig": {
                    "user": "root:root",
                    "tty": false,
                    "entrypoint": "sleep",
                    "arguments": [
                        "10"
                    ],
                    "privileged": true
                },
                "Output": "",
                "OpenStdin": false,
                "ID": "af161f8029c9f845531d09b801594363dd09a0865a9f6c30e11119d1a9966457",
                "ContainerID": "a6c71c6f032a49487bc49d51d4de6d763a44e59addfc4a1c1b161a0728499f66"
            },
            {
                "OpenStderr": true,
                "OpenStdout": true,
                "ContainerId": "ece76b382bc599702e2a451d627bd83f77ce1faf1a93e867574688ba46cf5112",
                "DetachKeys": "",
                "ExitCode": 0,
                "Pid": 32161,
                "NodeId": "wn99oc5gv7u0ugt7yih5ymdw4",
                "CanRemove": false,
                "Running": false,
                "ProcessConfig": {
                  "user": "root:root",
                  "tty": false,
                  "entrypoint": "sleep",
                  "arguments": [
                    "10"
                  ],
                  "privileged": true
                },
                "Output": "",
                "OpenStdin": false,
                "ID": "4893141a3930c4128b16ae1e3c01df0f494f5fb4b1573651b9d5261d791f5d3c",
                "ContainerID": "ece76b382bc599702e2a451d627bd83f77ce1faf1a93e867574688ba46cf5112"
            },
            {
                "NodeId": "wn99oc5gv7u0ugt7yih5ymdw4",
                "ContainerId": "c2ed986a541c8336f8f2c88230de1a53bfd0c8d6929d2c7bda09185cbf3c8c5c",
                "ID": "980d0317a8bbac3a20bfac5134881219c7dfb7c85598270f03ea0e0ab1152b66"
            },
            {
                "NodeId": "wn99oc5gv7u0ugt7yih5ymdw4",
                "ContainerId": "4b9f9b3978f13324782beeadb2c7d612287d2b0ad1daea1d700e00352c1ba011",
                "ID": "aaaaa8636b993526d7f860a7b19f5c5049ab06f83f298523cbc3dd3f39203823"
            },
            {
                "NodeId": "guv4tovwx67oa4j9evjrcgg5v",
                "ContainerId": "10fead3fd22f4e43b91019a642081b5759dd1bff25c23e5ddceb67164979e41a",
                "ID": "95671dbcc058031259592d0389ca0a674deb1e1e44229d61a199dbf4e0669762"
            }
        ]
    }
404
    job_id_not_found
        - { jobId } # 作业 ID 未找到
    executor_id_not_found
        - { executorId } # 作业执行结果 ID 未找到
```

### 下载日志
```
GET /api/jobs/<job-id>/log/<executor-id>?ContainerId=<container-id>


```