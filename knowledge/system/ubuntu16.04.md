---
    ubuntu16使用过程新增的额外配置（root）
---


### 1 网络
#### 1.1 xinetd
原因：为了测试UNP中的某些程序，需要daytime服务
安装和配置：
```shell
    sudo aptitude install xinetd
    
    // 开启TCP服务
    sudo vim /etc/xinetd.d/daytime
    // 重启xinetd
    sudo /etc/init.d/xinetd restart
    sudo /etc/init.d/xinetd status
```
