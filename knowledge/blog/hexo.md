---
title: hexo部署说明
date: 2016-12-05 17:00:00
tags: shell
---

欢迎来到狂想的个人实验室。  
github：[unlessbamboo](https://github.com/unlessbamboo)


### 1 Introduction
> 系统环境ubuntu16.04
> 另外，请将该文档补充到印象笔记《blog-personal blog》中
#### 1.1 what is hexo?
hexo是什么？如何安装hexo?
#### 1.2 How create a web?
如何利用hexo建立简易博客？需要做哪些配置？
Hexo相关命令?
#### 1.3 Glossary
相关术语介绍
#### 1.4 Tag Plugins
标签插件，并非front-matter中的tags。用于在文章中插入各种指定内容。
#### 1.5 themes
主题的下载以及配置
#### 1.6 third service
第三方服务


### 2 What is hexo?
> 注意，hexo项目本身的代码不要使用git管理，不然后面会出现问题。
#### 2.1 hexo
hexo是一个快速、简洁且高效的博客框架，使用Markdown或者其他渲染引擎
解析文章，并生成静态页面。
#### 2.2 Install
##### 2.2.1 Requirement
按照git和node.js
```shell
    # 按照git
    sudo aptitude install git-core

    # 按照nvm
    cd /tmp/
    wget -qO- https://raw.github.com/creationix/nvm/master/install.sh
    chmod +x install.sh
    ./install.sh

    # 利用nvm按照node.js，如果发现/usr/bin/nodejs不存在，注意软连接
    # 此情况在是哟哦你给sudo aptitude install npm时会出现
    nvm install stable
```
##### 2.2.2 hexo
```shell
    # 全局安装
    npm install -g hexo-cli
```


### 3 How create a web?
#### 3.1 Initialize
初始化网站的各个配置文件和相关目录，命令如下：
```shell
    # init，新建一个网站
    hexo init blog
    cd blog

    # install web, if support git, use:
    # npm install helo-deployer-git --save
    npm install
```
各个文件夹含义：
```
    _config.yml         配置信息，见<https://hexo.io/zh-cn/docs/configuration.html>说明
    package.json        应用程序信息
    scaffolds           模板文件夹，hexo依据这来创建文件
    source              存放用户资源的地方
    themes              主题
```
#### 3.2 基本命令
```shell
    # 新建一篇文章
    hexo new [layout] <title>

    # 根据markdown资源生成所有的静态文件
    hexo generate

    # 发布草稿
    hexo publish [layout] <filename>

    # 启动hexo服务器
    hexo server

    # 部署网站，根据配置，此时上传到服务器上的文件是一个成型的网站
    # (日期文件夹、archives、css、images、js、index.html文件）等
    hexo deploy

    # 渲染
    hexo render <file1> <file2> ..

    # 迁移
    hexo migrate <type>

    # 清除缓存文件、静态文件
    hexo clean

    # 列出网站的资料
    hexo list <type>
```
#### 3.3 选项
```shell
    # 安全模式，不会插入脚本和插件
    hexo --safe

    # 调试模式
    hexo --debug

    # 简洁模式
    hexo --silent

    # 自定义配置文件路径
    hexo --config custom.yml

    # 显示草稿
    hexo --draft
```


### 4 Glossary
#### 4.1 layout
布局，有：post, page, draft，对应不同的路径
```
    post            source/_posts
    page            source
    draft           source/_drafts
```
#### 4.2 Scaffold
模板，根据scaffolds文件夹来创建文件，例如
```
    # 会在scaffolds文件夹中查找photo.md文件来创建文章
    hexo new photo "my a"
```
#### 4.3 Front-matter
文件最上方使用---分割的区域，指定个别文件的变量，参数说明：
```
    layout              文件布局
    title               标题
    date                建立日期(默认值为文件建立日期）
    updated             更新日期（默认值文件更新日期）
    comments            开启文章的评论功能(true)
    tags                标签（不适用于分页）
    categories          分类（不适用于分页）
    permalink           覆盖文章网址
    photos              在文章头部插入图片
```
##### 4.3.1 标签和分类
分类具有层次性，标签则无，如果添加多个标签：
```
    tags:[python, javascript]
    或者
    tags:
    - python
    - javascript
```
##### 4.3.2 标签
添加标签页面的命令如下：
```shell
    hexo new page tags
    # 此时，会在source/tags/生成index.md文件，修改该文件内容
```
##### 4.3.3 分类
添加分类页面的命令如下：
```shell
    hexo new page categories
    # 此时，会在source/categories/下生成index.md文件，修改
```

#### 4.4 source
##### 4.4.1 资源
资源+文章内容，其中资源表示：图片，CSS等文件
##### 4.4.2 数据文件
source/\_data文件夹，用于不在文章内，但是重复使用的资料。


### 5 Tag Pugins
#### 5.1 quote
插入引言，可以包含（作者，来源，标题等）
```
    {% blockquote [author[, source]] [link] [source_link_title] %}
    content
    {% endblockquote %}
```
#### 5.2 Code
代码块
```
    {% codeblock [title] [lang:language] [url] [link text] %}
    code snippet
    {% endcodeblock %}
```
#### 5.3 反引号
就是一直在使用的三个反引号, 具体格式：
```
    ```[language][title][url][link text] code```
```
#### 5.4 others
```
    # youtube视频
    {% youtube video_id %}

    # 文章
    {% post_path slug [title] %}

    # 资源
    {% assert_img slug [title] %}
```


### 6 themes
#### 6.1 downloads
例如下载next主题，命令如下：
```shell
    # 方法1：https://github.com/iissnan/hexo-theme-next/releases 下载

    # 方法2
    cd hexo
    git clone https://github.com/iissnan/hexo-theme-next themes/next
```
#### 6.2 configure
在config.yml中，修改themes项配置信息
#### 6.3 rss
在相应的themes目录下的config.yml中有rss选项


### 7 Third Service
#### 7.1 多说
登陆多说官网，注册用户名，其中站点地址为(github pages)地址；之后
在config.yml添加duoshuo_shortname字段即可。
```gcc
    # 用户名（unusebamboo，目前使用qq：1647403840来登陆，谷歌太慢）

    # 配置
    duoshuo_shortname: unlessbamboo
```
#### 7.2 访客统计
[不蒜子](http://ibruce.info/2015/04/04/busuanzi/)  


### 8 部署
#### 8.1 github
##### 8.1.1 github pages说明
每一个github账号只能有一个特殊的命令约定项目：username.github.io，用于
创建个人博客，所有网站内容在master分支下（当然，另外一种gh-pages这里
不再描述）。  
在创建完项目之后，可以在setting中查看是否正确的完成部署操作。  
##### 8.1.2 pages原理
- master下的静态文件可以通过username.github.io链接访问
- hexo -g会生成一个静态网站
- hexo d会将静态网站提交到github上

##### 8.1.3 dns绑定
[参考](https://help.github.com/articles/troubleshooting-custom-domains/)  
在获取相应的ip地址信息后，在相应域名服务商上面设置即可。
```shell
    # 获取ip地址
    dig https://unlessbamboo.github.io +nostats +nocomments +nocmd

    # dnspod上设置的CNAME默认值为
    unlessbamboo.github.io.

    # @记录值，指定为上面的IP地址
```
##### 8.1.4 cname设置
在hexo项目source/下创建CNAME文件，加入"www.unusebamboo.com"，以便
能够顺利的访问。

#### 8.2 coding
[参考coding](https://coding.net/help/doc/pages/index.html)  
在创建同用户名的项目之后，进入pages服务项，选择部署来源，最后
绑定域名访问地址：www.unusebamboo.com，当然，首先得保证dns配置。
