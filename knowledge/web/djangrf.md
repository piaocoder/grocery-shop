---
title: django rest framwork知识
tags: xinshu
---


### 1, Introduction



### 2, 目录结构说明
#### 2.1 目录结构
```
	.
	├── __init__.py
	├── apis.py
	├── config.py
	├── models.py
	├── permissions.py
	├── serializers.py
	├── services.py
	├── urls.py
	├── validators.py
	└── views.py
```
#### 2.2 说明
apis.py代替views.py，在urls.py中被使用；
services.py封装了models.py的处理逻辑，处于api和model的中间层；



viewsets说明：
    功能：
        REST framework includes an abstraction for dealing with ViewSets, 
        that allows the developer to concentrate（专注于） on modeling the state 
        and interactions（交互） of the API, 
        and leave the URL construction(构建) to be handled automatically, 
        based on common conventions(约定).

    特点：
        提供create/update/retrieve/destory等方法替换正常view class中的put/get方法。
        现有方法如下：
            create、list、destory、retrieve、update


Routers说明：
    任何被list_route和detail_route修饰的函数都能被routed，其中两者的URL不同：
        list_route——{prefix}/{methodname}
        detail_route——{prefix}/lookup/{methodname}
