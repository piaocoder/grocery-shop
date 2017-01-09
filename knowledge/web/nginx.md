---
title: nginx配置说明  
time: 2016-12-26 21:11:00  
tags: 配置
---


### 1 Introduction


### 2 请求配置
#### 2.1 来源ip
##### 2.1.1 功能
一般而言，web服务器看到的ip地址都是代理服务器的ip地址，
而不是客户端的。当然，如果中间代理服务器为了支持来源
ip地址，可以添加x-forwarded-for字段，告知服务器。
配置如下：
```shell
    # nginx作为代理服务器，向后转换真实ip地址
    proxy_set_header Host       $host
    proxy_set_header X-Real-Ip  $remote_addr
    # 经过的所有ip地址，用,隔开，必须保证中间都用nginx
    proxy_set_header x-forwarded-for    $proxy_add_x_forwarded_for
```
##### 2.1.2 缺点
一般而言，不会使用客户端ip来在会话之间跟踪用户的行为，
因为ip地址无法确定的地方太多。另外，IP地址很容易伪造。
详细信息见《http权威讲解》275页
#### 2.2 host
##### 2.2.1 功能
一个IP地址对应多个域名，其中host字段在Apache等web服务器中起到
区分网站的用途。如果缺失该字段，返回400(bad request)。
##### 2.2.2 例子
```
    host:
```
