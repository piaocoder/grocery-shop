---
title: flask
date: 2016-10-29 18:00:00
tags: python
---


### 1 Introduction
- flask术语
- 设计理念
- app


### 2 Glossary
#### 2.1 wsgi
WSGI：Web Server Gateway Interface，标准接口规范，
规定了web服务器和python web应用/框架之间传递数据的规则，
一边python web应用可以和任何的web服务器（nginx，apache）配合工作。  
拓扑结构：
```
    Http客户端<------>web服务器<------->WSGI<------->Flask应用
```
#### 2.2 信号
##### 2.2.1 信号的处理
###### 2.2.1.1 定义
信号通过发送发生在核心框架的其他地方或者Flask扩展的动作时出发的
通知来帮助你解耦应用。
###### 2.2.1.2 主要用途
通知订阅者，而不鼓励订阅者修改数据；
###### 2.2.1.3 主要优势
信号相比其他处理器的最大优势是在不同的时段上安全的订阅，例如：
```
    单元测试中的临时订阅；
    了解哪个模块被作用请求的一部分渲染；
```
##### 2.2.2 信号的使用
###### 2.2.2.1 创建信号
使用blinker库来在自己的应用中使用信号
```python
    from blinker import Namespace
    mySignals = Namespace()
    # my signal
    sobj = mySignals.signal('sobj')
```
###### 2.2.2.2 发送信号
sobj.send(发送端对象，其他参数），例如：
```python
    # 在发送信号的类
    sobj.send(self)
    # 随机函数中
    sobj.send(current_app._get_current_object())
```
###### 2.2.2.3 订阅信号
使用connect_via装饰器方法来订阅信号
```python
    @template_rendered.connect_via(app)
    def when_template_rendered(sender, template, context, **extra):
        print 'Template %s is rendered with %s' % (template.name, 
                                                   context)
```
##### 2.2.3 信号分类
flask.template_rendered:  
模块成功渲染时，该信号会发出，其一般和模板实例
template/上下文字典context一起调用

flask.request_started:  
在除请求上下文之外的任何请求处理开始之前被调用，
因为此时请求上下文已经初始化完成，固可以使用request
标准全局代理访问请求并获取信息:
```python
    def log_request(sender, **extra):
        sender.logger.debug("Request context is up')

    from flask import request_started
    request_started.connect(log_request, app)
```

#### 2.3 应用上下文
> Flask的设计理念之一：整个Flask运行期间存在两个status（应用上下文/请求上下文）

##### 2.3.1 原因
见3.2.1说明
##### 2.3.2 创建
隐式创建：当请求上下文压栈时，如果有必要应用上下文就会被创建；
显示创建：
```python
    app.app_context()
    print current_app.name
```
##### 2.3.3 作用域：
自动创建和销毁，不会跨线程，不会在不同的请求之间共享；  
- 原理——应用上下文内存存在栈对象flask.app_ctx_stack，任何不同的扩展可以在其中存储额外的信息；  
- 扩展开发和用户开发的不同——flask.g对象是留给flask用户的代码使用的；上下文应用中的栈对象则是给扩展存储信息，以及其他用途。

##### 2.3.4 用法
缓存一些资源，例如数据库连接，过程如下：  
- 创建并缓存隐式资源，如果资源被释放，重新分配；
- 销毁资源；

例子：
```python
    def get_db():
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = connect_to_database()
        return db 

    @app.teardown_appcontext
    def teardown_db(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    # 或者使用LoacalProxy类来更加隐藏的分配数据库句柄：
    from werkzeug.local import LocalProxy db = LocalProxy(get_db)
```

#### 2.4 请求上下文
##### 2.4.1 定义
代码执行的第二个状态（第一个为程序上下文），此时上下文的本地对象
（flask.request，其他）指向当前请求；

##### 2.4.2 工作方式
函数实现：  
```python
    def wsgi_app(self, env):
        # request_context返回一个RequestContext上下文对象，
        # 结合with来绑定上下文
        # 该上下文作用对象在整个with（完成请求，单一线程）处理期间
        with self.request_context(env):
            try:
                rsp = self.full_dispatch_request()
            except Exception,e:
                rsp = self.make_response(self.handle_exception(e))
            return response(env, start_response)
```
请求上下文的栈：  
```
    栈顶表示当前活动的请求-->push将上下文入栈---->处理请求
        ----->pop将上下文出栈 
        ----->在出栈的同时肯定会调用teardown_request绑定的回调函数；
        
    PS：在请求上下文压栈之前，会隐式的创建应用上下文
```

#### 2.5 交互式shell
##### 2.5.1 前奏
所有的Flask程序都必须创建一个app程序实例（显示调用，
flask的设计理念之一），其中首参数用于决定app所在的根目录，
以便后期的资源查找，当然你也可以随便设置一个值，后果自负。  
##### 2.5.2 使用
```python
    # 1，初始化app
    # 注意：最好提前编写一个hello.py文件，从该文件中导入制定的app
    import flask
    from flask import Flask
    app = Flask('bamboo')

    # 2，创建请求上下文
    ctx = app.test_request_context()
    ctx.push()#入栈
    app.preprocess_request()#处理请求，返回rsp
    app.process_response(app.reponse_class())
    # 出栈，销毁上下文，见teardown_request()说明
    ctx.pop()

    # 3，查看程序名
    app.name或者current_app.name

    4，注意：
    # 一般程序上下文（current_app）的初始化都必须先于请求上下文完成，
    # 这里test_request_context应该默认包含了程序上下文的初始化工作，
    # 不然current_app.name会抛出异常信息
```

#### 2.6 路由
##### 2.6.1 定义
route是一个装饰器，用于对给定的URL规则进行view函数注册。
```python
    flask.Flask.route(rule, *options)；
    flask.Flask.add_url_url()；
    flask.Flask.url_map，底层的Werkzeug路由系统；
```
##### 2.6.2 rule的规则
###### 2.6.2.1 规则  
```
    a）普通字符串url：/，/usr/
    b）变量形式字符串：
        /usr/<username>，username可以是一个转换器<converter:username>
```
###### 2.6.2.2 其他参数  
```
    endpoint：  注册的URL规则的末端，具体见后面的说明；
    view_func： 请求递交到endpoint时调用的函数，见add_url_rule说明
    defaults：  规则默认值的字典，例如：
        @app.route('/users/', defaults={'pagenum': 1})
        @app.route('/users/page/<int:pagenum>)
        def show_users(pagenum):
            pass
        其中/users/表示第一页的资源，/users/page/N表示第N页的URL
    subdomains:
                当使用子域名匹配时，为子域名设定规则，如果没有指定，
                默认的子域名
    **options:  选项值，推送给底层的rule对象（werkzeug）
```
##### 2.6.3 工作方式：
flask中路由的设计理念（werkzeug）是将指定的URL规则映射到某一个
逻辑对象中，以便运行。
```python
        # 1，views decorator和add_url_rule
        # 装饰器视图：
        @app.route('/bamboo/<name>')
        def my_bamboo(name):
            pass
        # 上面的视图等价与下面的操作：
        def my_bamboo(name):
            pass
        app.add_url_rule('/bamboo/<name>', 'my_bamboo', my_bamboo)
                      
        """
        2, 此时访问url：http://unlessbamboo.com/bamboo/bifeng，
           此时flask会取出bamboo/bifeng
           并传递给指定的函数进行处理，那么整个处理逻辑时什么呢？
            a）不是的：
                http://unlessbamboo.com/bamboo/bifeng被视图
                my_bamboo处理；
            b）正确的：
                http://unlessbamboo.com/bamboo/bifeng被EndPoint
                （my_bamboo）处理；
            c) 解释
                到达EndPoint的请求将会被视图函数my_bamboo处理
                即后台进行里封装和转移操作；
        """
```
##### 2.6 4 EndPoint
[引用](http://stackoverflow.com/questions/19261833/what-is-an-endpoint-in-flask)  
```
根据《rule工作方式》，可以得到:
    1, EP是一个唯一表示，用于决定使用那个处理逻辑去应对对应的请求。  
    2，显示的指定EP之后：
        @app.route('/bamboo/<name>', endpoint='say_hello')
        def my_bamboo(name):
            pass
        此时的处理过程如下：
            http://unlessbamboo.com/bamboo/bifeng将会被
            EndPoint(say_hello）处理
            -->say_hello映射到视图函数my_bamoo，再处理；

    3，为何有该选项（默认不可以吗？）
        用于更加高级的用法，BluePrints就是基于EndPoint，
        将应用分成不同的独立个体，几次此时views函数时一样的。
```

##### 2.6.5 converter
变量转换器，将匹配的url中的参数变量转为相应的值；
```
    <string:name>           默认项，转为string类型
    <int:age>,<float:weigth>
    <path:name>             类似string，但是接受斜线字符串
```

##### 2.6.6 url的斜线匹配规则
web服务器处理静态文件时，保证安全的使用相对链接地址（URL自动拼接）
```
    如果有：URL规则中如果有斜线，所有请求都转到这里；
    如果没有：此时如果用户带了斜线，404错误
```

#### 2.7 即插视图
出发点：
    构造一个通用的，适应其他模板和模型的视图，从而具有更大的灵活性

#### 2.8 模板

#### 2.9 工厂函数
##### 2.9.1 定位
增加模块开发的灵活性，以适用于不用的情景（测试，多个app（v1.0，v1.1）），
此时可以在应用的__init__.py中复制代码完成app的创建，
但是有一种更好的方法即使用“工厂函数”
##### 2.9.2 创建
```python
    def create_app(config):
        app = Flask(__name__)
        app.config.from_pyfile(config)

        from youapp.views.admin import admin
        from youapp.views.fronted import fronted
        app.register_blueprint(admin)
        app.register_blueprint(fronted)

        return app

    #此时在蓝图中可以使用代理对象current_app
```
##### 2.9.3 使用
```python
    from youapp import create_app
    app = create_app('/path/to/config')
    app.run()
```


### 3 设计理念
#### 3.1 设计理念
##### 3.1.1 应用和请求
整个flask运行期间存在两个status（应用配置和请求配置）
##### 3.1.2 微
微框架——保证flask核心简单而且易于扩展，flask本身不会给你做太多
决策（使用何种引擎，使用何种数据库）
##### 3.1.3 pythonic
> 让简单的任务保持简单，不会对你做出过多的限制。

flask尽可能提供一个非常简单的胶水层，这本来也是python的品质之一。

#### 3.2 设计支柱
##### 3.2.1 单进程多应用
设计支柱之一——一个python进程存在多个应用。  
需求：如何在多个应用中正确的匹配指定的应用？  
解决办法1:
```
    在请求上下文中附加很多函数，用于显示的传递应用。
    但是很多扩展不适用参数传递方式，该方法不能解决此类问题。
```
解决办法2：current_app代理，应用上下文。  



### 4 app
#### 4.1 工具
##### 4.1.1 virtualenv
见印象笔记-编程语言-python-python切换工具笔记，后期补充该节内容。
