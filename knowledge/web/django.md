---
title: django
date: 2017-o1-12 06:09:00
tags: python
---


### 1 Introduction



### 2 settings
django中settings.py文件的介绍。  
在配置文件中可以使用普通的Python语法，但是不能有语法错误。  
#### 2.1 加载过程
django的默认配置都在django/conf/global_settings.py中，会
被自定义的settings.py覆盖某些字段，django启动时加载顺序：
- global_settings.py
- settings.py

##### 2.1.1 setting位置
```python
    # 1, manager.py文件
    # 配置文件位置通过变量DJANGO_SETTINGS_MODULE告知django。
```
##### 2.1.2 配置区别
可以使用如下命令查看当前配置和默认配置的区别
```shell
    python manage.py diffsettings
```
##### 2.1.3 自定义配置
自定义配置惯例：
- 名称用大写
- 不要使用已存在的配置
- 尽量使用元祖来表示序列

#### 2.2 基本配置
##### 2.2.1 基本
```python
    # 1, PASSWORD_HASHER密码加密算法列表，默认使用PBKF2
    #   例如make_password,check_password,is_password_unable中使用  
    PASSWORD_HASHER = {
        'django.contrib.auth.hashers.PBKDF2PasswordHasher',
		'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
		'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
		'django.contrib.auth.hashers.BCryptPasswordHasher',
		'django.contrib.auth.hashers.SHA1PasswordHasher',
		'django.contrib.auth.hashers.MD5PasswordHasher',
		'django.contrib.auth.hashers.CryptPasswordHasher',
    }

    
    # 2, ADMINS，开发人员的姓名和邮件，在DEBUG为Fasle时，如果
    #       views发送异常时发送邮件；
    #    MANAGERS，出现broken link时发送邮件，类似ADMINS
    ADMINS = (('John', 'john@example.com'), ('Mary', 'mary@example.com'))
    MANAGERS = (('John', 'john@example.com'), ('Mary', 'mary@example.com'))


    # 3, ALLOWED_HOSTS，限定请求中的host值，仅仅列表中的host才可以访问
    #   缓存污染：控制缓存系统将恶意页面返回给用户
    #   密码重置：发送给用户的内容污染，间接的劫持邮件发送内容
    ALLOWED_HOSTS = [
        '.example.com',  # Allow domain and subdomains
        '.example.com.',  # Also allow FQDN and subdomains
    ]


    # 4, DEBUG,调试开关
    #    TEMPLATE_DEBUG，是否在网页上显示debug信息
    DEBUG = True
    TEMPLATE_DEBUG = True

    
    # 5, INSTALLED_APPS，一元数组，应用应该加载的自带或者自定app列表
    #   使用应用注册表进行自我检查，代码中使用django.apps.apps来访问
    INSTALLED_APPS = [
        apps.user,
    ]


    # 6, MIDDLEWARE_CLASSES，django运行过程中需要加载的中间件列表
    #   或者定制的中间件包路径
    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
    )

    # 7, SESSION_COOKIE_SECURE，使cookie标记上secure标志，从而
    #       在https下面传输
    #    SESSION_COOKIE_HTTPONLY仅仅被http读取，不能被js读取
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True

    # 8，CACHE缓存嵌套字典，将高速缓存别名映射到包含单个高速缓存的选项字典中
    #   必须设置default项
    CACHE = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            # 使用缓存的目录或者文件
            'LOCATION': '/var/tmp/django_cache',
            # 高速缓存有效时间
            'TIMEOUT': 300
        }
    }

    # 9, DATABASES，包含数据库配置，必须包含一个default项
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'mydb',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        },
    }

    # 10，邮件发送
    # 发送邮件后端
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    # 后端保存输出目录
    EMAIL_FILE_PATH = ''
    # 发送邮件使用的主机
    EMAIL_HOST = 'localhost'
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    EMAIL_PORT = 25
    # Transport Layer Security连接
    EMAIL_USE_TLS = True
    # 超时
    EMAIL_TIMEOUT = 1

    # 模板
```
##### 2.2.2 文件相关
```python
    # 从磁盘读取文件时的解码方式
    FILE_CHARSET = 'utf-8'
    # 文件上传操作
    FILE_UPLOAD_HANDLERS = (
        "django.core.files.uploadhandler.MemoryFileUploadHandler",
        "django.core.files.uploadhandler.TemporaryFileUploadHandler"
    )
    FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440
    FILE_UPLOAD_TEMP_DIR = "/tmp"
```
##### 2.2.3 日志相关
```python
    # 日志配置字典
    LOGGING = {}
    # 日志配置的回调对象
    LOGGING_CONFIG = 'logging.config.dictConfig'
```

#### 2.3 中间件推荐
##### 2.3.1 SessionMiddleware
配置作用：在应用中使用session  
配置方法：
```python
    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
    )
```
##### 2.3.2 CsrfViewMiddleware
配置作用：在应用中添加CSRF token来防范csrf攻击  
配置方法：
```python
    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.CsrfViewMiddleware',
    )
```
##### 2.3.3 clickjacking.XFrameOptionsMiddleware
作用：在http header中添加X-Frame-Options，防范Clickjacking  
配置方法：
```python
    MIDDLEWARE_CLASSES = (
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )
```
