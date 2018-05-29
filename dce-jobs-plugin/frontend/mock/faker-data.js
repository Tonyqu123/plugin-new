/* eslint-disable */
  // "/jobs/:JobId": "/jobs/:JobId",

module.exports = function () {
  var faker = require("faker");
  faker.locale = "zh_CN";
  var _ = require("lodash");
  return {
    jobs: _.times(100, function (n) {
      var ExecutorsList = _.times(6, function() {
        return faker.random.uuid();
      });
      const id = faker.random.uuid();
      return {
        id,
        JobId: id,
        ServiceName: faker.random.objectElement(),
        Name: faker.random.word(),
        Cmd: 'ps axu',
        Privileged: faker.random.boolean(),
        User: 'root:root',
        Env: ['a=b', 'c=d'],
        SecretArgs: ['xxx', 'yyy'],
        Executors: ExecutorsList,
      };
    }),
    apps: {
      "Services": [
        {
          "Endpoint": {
            "VirtualIPs": [
              {
                "NetworkID": "nce3aumx1k13sg31weattgtui",
                "Addr": "10.255.0.6/16"
              }
            ],
            "Spec": {
              "Mode": "vip",
              "Ports": [
                {
                  "TargetPort": 80,
                  "Protocol": "tcp",
                  "PublishMode": "ingress"
                }
              ]
            },
            "Ports": [
              {
                "TargetPort": 80,
                "PublishedPort": 30002,
                "Protocol": "tcp",
                "PublishMode": "ingress"
              }
            ]
          },
          "ID": "lppzzwx6qyk3blovyhk2flmjx",
          "Version": {
            "Index": 1400857
          },
          "PreviousSpec": {
            "Name": "2048_game2048",
            "EndpointSpec": {
              "Mode": "vip",
              "Ports": [
                {
                  "TargetPort": 80,
                  "Protocol": "tcp",
                  "PublishMode": "ingress"
                }
              ]
            },
            "Labels": {
              "com.docker.stack.namespace": "2048",
              "io.daocloud.dce.authz.owner": "admin",
              "io.daocloud.dce.template": "2048"
            },
            "UpdateConfig": {
              "MaxFailureRatio": 0,
              "Parallelism": 1,
              "FailureAction": "pause"
            },
            "Mode": {
              "Replicated": {
                "Replicas": 1
              }
            },
            "TaskTemplate": {
              "Placement": {},
              "ContainerSpec": {
                "Image": "daocloud.io/daocloud/dao-2048:latest@sha256:7b26f2e4a5035819ef496efdba8d3da8e94fa0141a1b55bb5b01f8956f77c413",
                "Labels": {
                  "com.docker.stack.namespace": "2048",
                  "io.daocloud.dce.authz.owner": "admin",
                  "io.daocloud.dce.template": "2048"
                },
                "DNSConfig": {}
              },
              "LogDriver": {
                "Name": "json-file"
              },
              "RestartPolicy": {
                "MaxAttempts": 0,
                "Condition": "any"
              },
              "ForceUpdate": 0,
              "Resources": {
                "Limits": {
                  "MemoryBytes": 1073741824,
                  "NanoCPUs": 500000000
                }
              }
            }
          },
          "UpdatedAt": "2017-06-06T03:11:20.618485808Z",
          "UpdateStatus": {
            "StartedAt": "0001-01-01T00:00:00Z",
            "CompletedAt": "0001-01-01T00:00:00Z"
          },
          "Spec": {
            "Name": "2048_game2048",
            "EndpointSpec": {
              "Mode": "vip",
              "Ports": [
                {
                  "TargetPort": 80,
                  "Protocol": "tcp",
                  "PublishMode": "ingress"
                }
              ]
            },
            "Labels": {
              "com.docker.stack.namespace": "2048",
              "io.daocloud.dce.authz.owner": "admin",
              "io.daocloud.dce.template": "2048"
            },
            "UpdateConfig": {
              "MaxFailureRatio": 0,
              "Parallelism": 1,
              "FailureAction": "pause"
            },
            "Mode": {
              "Replicated": {
                "Replicas": 5
              }
            },
            "TaskTemplate": {
              "Placement": {},
              "ContainerSpec": {
                "Image": "daocloud.io/daocloud/dao-2048:latest@sha256:7b26f2e4a5035819ef496efdba8d3da8e94fa0141a1b55bb5b01f8956f77c413",
                "Labels": {
                  "com.docker.stack.namespace": "2048",
                  "io.daocloud.dce.authz.owner": "admin",
                  "io.daocloud.dce.template": "2048"
                },
                "DNSConfig": {}
              },
              "LogDriver": {
                "Name": "json-file"
              },
              "RestartPolicy": {
                "MaxAttempts": 0,
                "Condition": "any"
              },
              "ForceUpdate": 0,
              "Resources": {
                "Limits": {
                  "MemoryBytes": 1073741824,
                  "NanoCPUs": 500000000
                }
              }
            }
          },
          "CreatedAt": "2017-06-05T10:12:38.957099654Z"
        }
      ],
      "Name": "2048",
      "Tenant": null
    },
    start: {
      "SecretArgs": [
        "*",
        "**",
        "***"
      ],
      "Name": "\u4e0a\u7ebfxxxxxx",
      "Executors": [
        "1496910345",
        "1496911768",
        "1496912866",
        "1496913547",
        "1496913602",
        "1496913662"
      ],
      "Cmd": "ps axu",
      "JobId": "515ad5d7-a45f-4307-b6b2-ed5b2256a97e",
      "ServiceName": "2048_game2048",
      "User": "root:root",
      "Env": [
        "a=bbbbbbb",
        "c=d"
      ],
      "Privileged": true
    },
    target: {
      "JobId": "515ad5d7-a45f-4307-b6b2-ed5b2256a97e",
      "Result": [
        {
          "ContainerId": "8m1suwz2bjj2kcsrxz0z5iccs",
          "NodeId": "wn99oc5gv7u0ugt7yih5ymdw4"
        },
        {
          "ContainerId": "qdi0z3y3u3z3y23ws01n1cnnm",
          "NodeId": "wn99oc5gv7u0ugt7yih5ymdw4"
        },
        {
          "ContainerId": "r932w317v512dwnsteycvlpa9",
          "NodeId": "wn99oc5gv7u0ugt7yih5ymdw4"
        },
        {
          "ContainerId": "t3o2xbsnfo2vhon0y47v2ss7s",
          "NodeId": "wn99oc5gv7u0ugt7yih5ymdw4"
        },
        {
          "ContainerId": "z6y6485tcnhnjazv2kox67091",
          "NodeId": "guv4tovwx67oa4j9evjrcgg5v"
        },
      ],
      "CreateTime": 1497000579.575937,
      "Target": [
        {
          "ContainerId": "8m1suwz2bjj2kcsrxz0z5iccs",
          "NodeId": "wn99oc5gv7u0ugt7yih5ymdw4"
        },
        {
          "ContainerId": "qdi0z3y3u3z3y23ws01n1cnnm",
          "NodeId": "wn99oc5gv7u0ugt7yih5ymdw4"
        },
        {
          "ContainerId": "r932w317v512dwnsteycvlpa9",
          "NodeId": "wn99oc5gv7u0ugt7yih5ymdw4"
        },
        {
          "ContainerId": "t3o2xbsnfo2vhon0y47v2ss7s",
          "NodeId": "wn99oc5gv7u0ugt7yih5ymdw4"
        },
        {
          "ContainerId": "z6y6485tcnhnjazv2kox67091",
          "NodeId": "guv4tovwx67oa4j9evjrcgg5v"
        },
      ]
    },
    tasks: [
      {
        "Slot": 4,
        "Status": {
          "Timestamp": "2017-06-06T03:11:21.118722901Z",
          "State": "running",
          "ContainerStatus": {
            "PID": 10609,
            "ContainerID": "4b9f9b3978f13324782beeadb2c7d612287d2b0ad1daea1d700e00352c1ba011"
          },
          "Message": "started",
          "PortStatus": {}
        },
        "NodeID": "wn99oc5gv7u0ugt7yih5ymdw4",
        "ID": "8m1suwz2bjj2kcsrxz0z5iccs",
        "DesiredState": "running",
        "Version": {
          "Index": 1400863
        },
        "ServiceID": "lppzzwx6qyk3blovyhk2flmjx",
        "UpdatedAt": "2017-06-06T03:11:21.260256224Z",
        "NetworksAttachments": [
          {
            "Network": {
              "IPAMOptions": {
                "Configs": [
                  {
                    "Subnet": "10.255.0.0/16",
                    "Gateway": "10.255.0.1"
                  }
                ],
                "Driver": {
                  "Name": "default"
                }
              },
              "ID": "nce3aumx1k13sg31weattgtui",
              "Version": {
                "Index": 1397540
              },
              "UpdatedAt": "2017-06-06T02:52:12.257256091Z",
              "DriverState": {
                "Name": "overlay",
                "Options": {
                  "com.docker.network.driver.overlay.vxlanid_list": "4096"
                }
              },
              "Spec": {
                "IPAMOptions": {
                  "Configs": [
                    {
                      "Subnet": "10.255.0.0/16",
                      "Gateway": "10.255.0.1"
                    }
                  ],
                  "Driver": {}
                },
                "Labels": {
                  "com.docker.swarm.internal": "true"
                },
                "Name": "ingress",
                "DriverConfiguration": {}
              },
              "CreatedAt": "2017-04-19T07:09:42.703012452Z"
            },
            "Addresses": [
              "10.255.0.9/16"
            ]
          }
        ],
        "Spec": {
          "Placement": {},
          "ContainerSpec": {
            "Image": "daocloud.io/daocloud/dao-2048:latest@sha256:7b26f2e4a5035819ef496efdba8d3da8e94fa0141a1b55bb5b01f8956f77c413",
            "Labels": {
              "com.docker.stack.namespace": "2048",
              "io.daocloud.dce.authz.owner": "admin",
              "io.daocloud.dce.template": "2048"
            },
            "DNSConfig": {}
          },
          "LogDriver": {
            "Name": "json-file"
          },
          "RestartPolicy": {
            "MaxAttempts": 0,
            "Condition": "any"
          },
          "ForceUpdate": 0,
          "Resources": {
            "Limits": {
              "MemoryBytes": 1073741824,
              "NanoCPUs": 500000000
            }
          }
        },
        "CreatedAt": "2017-06-06T03:11:20.619318884Z"
      },
      {
        "Slot": 1,
        "Status": {
          "ContainerStatus": {
            "ContainerID": "0bde0479916ffb06e564f50c3c20e214c816a62a516dcb4e199a80ffdf005a10",
            "ExitCode": 255
          },
          "PortStatus": {},
          "Err": "task: non-zero exit (255)",
          "Timestamp": "2017-06-06T02:52:11.550428838Z",
          "State": "failed",
          "Message": "started"
        },
        "NodeID": "wn99oc5gv7u0ugt7yih5ymdw4",
        "ID": "qdi0z3y3u3z3y23ws01n1cnnm",
        "DesiredState": "shutdown",
        "Version": {
          "Index": 1397574
        },
        "ServiceID": "lppzzwx6qyk3blovyhk2flmjx",
        "UpdatedAt": "2017-06-06T02:52:13.369132122Z",
        "NetworksAttachments": [
          {
            "Network": {
              "IPAMOptions": {
                "Configs": [
                  {
                    "Subnet": "10.255.0.0/16",
                    "Gateway": "10.255.0.1"
                  }
                ],
                "Driver": {
                  "Name": "default"
                }
              },
              "ID": "nce3aumx1k13sg31weattgtui",
              "Version": {
                "Index": 1397540
              },
              "UpdatedAt": "2017-06-06T02:52:12.257256091Z",
              "DriverState": {
                "Name": "overlay",
                "Options": {
                  "com.docker.network.driver.overlay.vxlanid_list": "4096"
                }
              },
              "Spec": {
                "IPAMOptions": {
                  "Configs": [
                    {
                      "Subnet": "10.255.0.0/16",
                      "Gateway": "10.255.0.1"
                    }
                  ],
                  "Driver": {}
                },
                "Labels": {
                  "com.docker.swarm.internal": "true"
                },
                "Name": "ingress",
                "DriverConfiguration": {}
              },
              "CreatedAt": "2017-04-19T07:09:42.703012452Z"
            },
            "Addresses": [
              "10.255.0.8/16"
            ]
          }
        ],
        "Spec": {
          "Placement": {},
          "ContainerSpec": {
            "Image": "daocloud.io/daocloud/dao-2048:latest@sha256:7b26f2e4a5035819ef496efdba8d3da8e94fa0141a1b55bb5b01f8956f77c413",
            "Labels": {
              "com.docker.stack.namespace": "2048",
              "io.daocloud.dce.authz.owner": "admin",
              "io.daocloud.dce.template": "2048"
            },
            "DNSConfig": {}
          },
          "LogDriver": {
            "Name": "json-file"
          },
          "RestartPolicy": {
            "MaxAttempts": 0,
            "Condition": "any"
          },
          "ForceUpdate": 0,
          "Resources": {
            "Limits": {
              "MemoryBytes": 1073741824,
              "NanoCPUs": 500000000
            }
          }
        },
        "CreatedAt": "2017-06-05T10:12:38.958457789Z"
      },
      {
        "Slot": 2,
        "Status": {
          "Timestamp": "2017-06-06T03:11:22.126441876Z",
          "State": "running",
          "ContainerStatus": {
            "PID": 10610,
            "ContainerID": "c2ed986a541c8336f8f2c88230de1a53bfd0c8d6929d2c7bda09185cbf3c8c5c"
          },
          "Message": "started",
          "PortStatus": {}
        },
        "NodeID": "wn99oc5gv7u0ugt7yih5ymdw4",
        "ID": "r932w317v512dwnsteycvlpa9",
        "DesiredState": "running",
        "Version": {
          "Index": 1400865
        },
        "ServiceID": "lppzzwx6qyk3blovyhk2flmjx",
        "UpdatedAt": "2017-06-06T03:11:22.265380596Z",
        "NetworksAttachments": [
          {
            "Network": {
              "IPAMOptions": {
                "Configs": [
                  {
                    "Subnet": "10.255.0.0/16",
                    "Gateway": "10.255.0.1"
                  }
                ],
                "Driver": {
                  "Name": "default"
                }
              },
              "ID": "nce3aumx1k13sg31weattgtui",
              "Version": {
                "Index": 1397540
              },
              "UpdatedAt": "2017-06-06T02:52:12.257256091Z",
              "DriverState": {
                "Name": "overlay",
                "Options": {
                  "com.docker.network.driver.overlay.vxlanid_list": "4096"
                }
              },
              "Spec": {
                "IPAMOptions": {
                  "Configs": [
                    {
                      "Subnet": "10.255.0.0/16",
                      "Gateway": "10.255.0.1"
                    }
                  ],
                  "Driver": {}
                },
                "Labels": {
                  "com.docker.swarm.internal": "true"
                },
                "Name": "ingress",
                "DriverConfiguration": {}
              },
              "CreatedAt": "2017-04-19T07:09:42.703012452Z"
            },
            "Addresses": [
              "10.255.0.11/16"
            ]
          }
        ],
        "Spec": {
          "Placement": {},
          "ContainerSpec": {
            "Image": "daocloud.io/daocloud/dao-2048:latest@sha256:7b26f2e4a5035819ef496efdba8d3da8e94fa0141a1b55bb5b01f8956f77c413",
            "Labels": {
              "com.docker.stack.namespace": "2048",
              "io.daocloud.dce.authz.owner": "admin",
              "io.daocloud.dce.template": "2048"
            },
            "DNSConfig": {}
          },
          "LogDriver": {
            "Name": "json-file"
          },
          "RestartPolicy": {
            "MaxAttempts": 0,
            "Condition": "any"
          },
          "ForceUpdate": 0,
          "Resources": {
            "Limits": {
              "MemoryBytes": 1073741824,
              "NanoCPUs": 500000000
            }
          }
        },
        "CreatedAt": "2017-06-06T03:11:20.619180298Z"
      },
      {
        "Slot": 1,
        "Status": {
          "Timestamp": "2017-06-06T02:52:20.102120778Z",
          "State": "running",
          "ContainerStatus": {
            "PID": 3615,
            "ContainerID": "ece76b382bc599702e2a451d627bd83f77ce1faf1a93e867574688ba46cf5112"
          },
          "Message": "started",
          "PortStatus": {}
        },
        "NodeID": "wn99oc5gv7u0ugt7yih5ymdw4",
        "ID": "t3o2xbsnfo2vhon0y47v2ss7s",
        "DesiredState": "running",
        "Version": {
          "Index": 1397622
        },
        "ServiceID": "lppzzwx6qyk3blovyhk2flmjx",
        "UpdatedAt": "2017-06-06T02:52:19.835100766Z",
        "NetworksAttachments": [
          {
            "Network": {
              "IPAMOptions": {
                "Configs": [
                  {
                    "Subnet": "10.255.0.0/16",
                    "Gateway": "10.255.0.1"
                  }
                ],
                "Driver": {
                  "Name": "default"
                }
              },
              "ID": "nce3aumx1k13sg31weattgtui",
              "Version": {
                "Index": 1397540
              },
              "UpdatedAt": "2017-06-06T02:52:12.257256091Z",
              "DriverState": {
                "Name": "overlay",
                "Options": {
                  "com.docker.network.driver.overlay.vxlanid_list": "4096"
                }
              },
              "Spec": {
                "IPAMOptions": {
                  "Configs": [
                    {
                      "Subnet": "10.255.0.0/16",
                      "Gateway": "10.255.0.1"
                    }
                  ],
                  "Driver": {}
                },
                "Labels": {
                  "com.docker.swarm.internal": "true"
                },
                "Name": "ingress",
                "DriverConfiguration": {}
              },
              "CreatedAt": "2017-04-19T07:09:42.703012452Z"
            },
            "Addresses": [
              "10.255.0.6/16"
            ]
          }
        ],
        "Spec": {
          "Placement": {},
          "ContainerSpec": {
            "Image": "daocloud.io/daocloud/dao-2048:latest@sha256:7b26f2e4a5035819ef496efdba8d3da8e94fa0141a1b55bb5b01f8956f77c413",
            "Labels": {
              "com.docker.stack.namespace": "2048",
              "io.daocloud.dce.authz.owner": "admin",
              "io.daocloud.dce.template": "2048"
            },
            "DNSConfig": {}
          },
          "LogDriver": {
            "Name": "json-file"
          },
          "RestartPolicy": {
            "MaxAttempts": 0,
            "Condition": "any"
          },
          "ForceUpdate": 0,
          "Resources": {
            "Limits": {
              "MemoryBytes": 1073741824,
              "NanoCPUs": 500000000
            }
          }
        },
        "CreatedAt": "2017-06-06T02:52:13.064028088Z"
      },
      {
        "Slot": 5,
        "Status": {
          "Timestamp": "2017-06-06T03:11:21.511366568Z",
          "State": "running",
          "ContainerStatus": {
            "PID": 27000,
            "ContainerID": "10fead3fd22f4e43b91019a642081b5759dd1bff25c23e5ddceb67164979e41a"
          },
          "Message": "started",
          "PortStatus": {}
        },
        "NodeID": "guv4tovwx67oa4j9evjrcgg5v",
        "ID": "z6y6485tcnhnjazv2kox67091",
        "DesiredState": "running",
        "Version": {
          "Index": 1400864
        },
        "ServiceID": "lppzzwx6qyk3blovyhk2flmjx",
        "UpdatedAt": "2017-06-06T03:11:21.563077148Z",
        "NetworksAttachments": [
          {
            "Network": {
              "IPAMOptions": {
                "Configs": [
                  {
                    "Subnet": "10.255.0.0/16",
                    "Gateway": "10.255.0.1"
                  }
                ],
                "Driver": {
                  "Name": "default"
                }
              },
              "ID": "nce3aumx1k13sg31weattgtui",
              "Version": {
                "Index": 1397540
              },
              "UpdatedAt": "2017-06-06T02:52:12.257256091Z",
              "DriverState": {
                "Name": "overlay",
                "Options": {
                  "com.docker.network.driver.overlay.vxlanid_list": "4096"
                }
              },
              "Spec": {
                "IPAMOptions": {
                  "Configs": [
                    {
                      "Subnet": "10.255.0.0/16",
                      "Gateway": "10.255.0.1"
                    }
                  ],
                  "Driver": {}
                },
                "Labels": {
                  "com.docker.swarm.internal": "true"
                },
                "Name": "ingress",
                "DriverConfiguration": {}
              },
              "CreatedAt": "2017-04-19T07:09:42.703012452Z"
            },
            "Addresses": [
              "10.255.0.10/16"
            ]
          }
        ],
        "Spec": {
          "Placement": {},
          "ContainerSpec": {
            "Image": "daocloud.io/daocloud/dao-2048:latest@sha256:7b26f2e4a5035819ef496efdba8d3da8e94fa0141a1b55bb5b01f8956f77c413",
            "Labels": {
              "com.docker.stack.namespace": "2048",
              "io.daocloud.dce.authz.owner": "admin",
              "io.daocloud.dce.template": "2048"
            },
            "DNSConfig": {}
          },
          "LogDriver": {
            "Name": "json-file"
          },
          "RestartPolicy": {
            "MaxAttempts": 0,
            "Condition": "any"
          },
          "ForceUpdate": 0,
          "Resources": {
            "Limits": {
              "MemoryBytes": 1073741824,
              "NanoCPUs": 500000000
            }
          }
        },
        "CreatedAt": "2017-06-06T03:11:20.619364005Z"
      },
      {
        "Slot": 3,
        "Status": {
          "Timestamp": "2017-06-06T03:11:22.441508077Z",
          "State": "running",
          "ContainerStatus": {
            "PID": 27032,
            "ContainerID": "a6c71c6f032a49487bc49d51d4de6d763a44e59addfc4a1c1b161a0728499f66"
          },
          "Message": "started",
          "PortStatus": {}
        },
        "NodeID": "guv4tovwx67oa4j9evjrcgg5v",
        "ID": "ziodljx20j6rgb9xf7hnylbq8",
        "DesiredState": "running",
        "Version": {
          "Index": 1400866
        },
        "ServiceID": "lppzzwx6qyk3blovyhk2flmjx",
        "UpdatedAt": "2017-06-06T03:11:22.468349341Z",
        "NetworksAttachments": [
          {
            "Network": {
              "IPAMOptions": {
                "Configs": [
                  {
                    "Subnet": "10.255.0.0/16",
                    "Gateway": "10.255.0.1"
                  }
                ],
                "Driver": {
                  "Name": "default"
                }
              },
              "ID": "nce3aumx1k13sg31weattgtui",
              "Version": {
                "Index": 1397540
              },
              "UpdatedAt": "2017-06-06T02:52:12.257256091Z",
              "DriverState": {
                "Name": "overlay",
                "Options": {
                  "com.docker.network.driver.overlay.vxlanid_list": "4096"
                }
              },
              "Spec": {
                "IPAMOptions": {
                  "Configs": [
                    {
                      "Subnet": "10.255.0.0/16",
                      "Gateway": "10.255.0.1"
                    }
                  ],
                  "Driver": {}
                },
                "Labels": {
                  "com.docker.swarm.internal": "true"
                },
                "Name": "ingress",
                "DriverConfiguration": {}
              },
              "CreatedAt": "2017-04-19T07:09:42.703012452Z"
            },
            "Addresses": [
              "10.255.0.12/16"
            ]
          }
        ],
        "Spec": {
          "Placement": {},
          "ContainerSpec": {
            "Image": "daocloud.io/daocloud/dao-2048:latest@sha256:7b26f2e4a5035819ef496efdba8d3da8e94fa0141a1b55bb5b01f8956f77c413",
            "Labels": {
              "com.docker.stack.namespace": "2048",
              "io.daocloud.dce.authz.owner": "admin",
              "io.daocloud.dce.template": "2048"
            },
            "DNSConfig": {}
          },
          "LogDriver": {
            "Name": "json-file"
          },
          "RestartPolicy": {
            "MaxAttempts": 0,
            "Condition": "any"
          },
          "ForceUpdate": 0,
          "Resources": {
            "Limits": {
              "MemoryBytes": 1073741824,
              "NanoCPUs": 500000000
            }
          }
        },
        "CreatedAt": "2017-06-06T03:11:20.61927821Z"
      }
    ]
  };
};
