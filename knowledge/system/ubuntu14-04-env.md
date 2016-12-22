---
title: Ubuntu 14.04下工作环境配置  
date: 2016-08-03 17:00:00
tags: 工作环境
---

欢迎来到狂想的个人实验室。  
github：[unlessbamboo](https://github.com/unlessbamboo)

## 一，Introduction
### 1.1 适用环境
Ubuntu 14.04.4 LTS x86-64

### 1.2 文章知识点
1. vim配置
2. browser和vim的结合
3. zshrc的配置
4. tmux在terminal上的应用

## 二，vim配置
> 总是要吃点猪肉的——没有最好的vim配置，只有自己一手逐渐累计搭建的vim插件集。
> 具体各个插件的配置以及说明后续文章《vim-插件管理》介绍，注意下文的[powerline配置](#p1234)。

### 2.0 效果图
![vim全景图](http://obbuzq2fl.bkt.clouddn.com/image/ubuntu14/vim%E5%85%A8%E5%B1%80.pngvim%E5%85%A8%E6%99%AF.png)

### 2.1 pathogen和git
> 虽然已有vundle管理插件实现自动化一体化的安装删除，但是本篇文章试用pathogen(~\_~)

#### 2.1.1 PG功能
pathogen——vim插件的加载器，保证每一个插件都在一个单独的目录中存放，降低了插件之间
的耦合度，简化了某一个插件的增加/删除。  

#### 2.1.2 PG+git原因
-   问题：
    pathogen仅仅是一个专注于插件加载的插件，提供简易的插件加载功能，不提供插件
的install,delete,update等功能。
-   解决办法：
    1)  使用vundle管理插件替换pathogen
    2)  结合git和pathogen来实现插件的加载，安装，删除，更新操作

#### 2.1.3 PG+git配置
> 假设第一次执行如下操作，如果仅仅时模块的更新克隆见后面章节介绍
-   克隆以及初始化vim远程仓库
``` bash
    cd .vim
    git init
    git remote add origin git@github.com:unlessbamboo/vim.git
    git pull origin master
```
-   安装pathogen
``` bash
    git submodule add https://github.com/tpope/vim-pathogen.git bundle/vim-pathogen
```
-   配置vimrc，见<https://github.com/tpope/vim-pathogen>的说明
``` vim
    runtime bundle/vim-pathogen/autoload/pathogen.vim
    execute pathogen#infect()
    syntax on
    filetype plugin indent on
```
-   安装其他插件（此时pathogen就已经开始生效了）
例如，安装bash-support插件用于支持shell脚本的编写
``` bash
    git submodule add https://github.com/vim-scripts/bash-support.vim.git bundle/bash-support
```
此时，会在bundle目录下生成bash-support目录

-   将当前.vim的所有修改push到远程仓库版本库中，从而一个ssh公钥在手，天下随便pull
``` bash
    git add .
    git commit -m 'shit.'
    git push origin master 
```

#### 2.1.4 插件检出
&emsp;在上面的操作结束后，你在本地已经有一份完整的vimrc配置。那么，如何一卡在手，走遍神州呢？  
&emsp;类似vundle，上文中将整个.vim作为一个git项目push到远程仓库版本库中就是为了方便版本库的克隆操作。
某一天，从地球到月球后：
``` bash
    # 克隆主项目
    git clone git@github.com:unlessbamboo/vim.git
    # 初始化子模块
    git submodule init
    # 更新所有子模块并检出
    git submodule update
```
> 当然有一种一劳永逸的办法，在克隆的时候同时拉取子模块：  
&emsp;git clone --recursive git@github.com:unlessbamboo/vim.git

#### 2.1.5 插件升级
&emsp;通过foreach语法，轮询对每一个子插件进行拉取：
``` bash
    git submodule foreach 'git checkout master && git pull'
```

#### 2.1.6 插件删除
-   手动删除对应配置:
    删除.gitmodules和.git/config中的引用信息
    rm -rf bundle/【插件名】
    提交更改到远程仓库版本库中；

-   自动删除
``` bash
    # 自动删除.gitmodules中的信息，但是不会删除本地.git/config中的信息
    # 但是不会将.git/config中的信息携带到月球上的，所以不用关心。
    git rm -rf bundle/[插件]
    git add .
    git commit -m 'a'
    git push origin master
```


### 三，browser配置
> 没有开发过前端，对browser了解很少，求介绍入坑，各种求  

#### 3.1   bookmark
xmarks，用于不同电脑，不同browser下的书签同步，如果你
仅仅使用一个browser，那么可以使用浏览器自带的书签同步，而且还会同步插件。  
> 已经弃置firefox，决定专心于chrome快捷键，但是这个还是保存着吧。

#### 3.2 fatkun
chrome下一款可以批量保存网页上所有图片并下载的，非常棒

#### 3.3 vim
-   名称：chrome(vimium)，firefox(vimfx)  
-   说明：脱离鼠标（cool），让你按照vim方式浏览插件，这是一款非常垃圾的插件，
不信你自己看，不管别人信不信，反正我信了。
-   效果图(通过按键来进行页面跳转)：  
![网页上的vim](http://obbuzq2fl.bkt.clouddn.com/ubuntu14/vimium%E6%95%88%E6%9E%9C.png)

#### 3.4 vpn
    > 非系统代理，仅仅限于浏览器
1.  shadowsocks代理软件，请自己查询购买，并在本地启动相应进程端口
2.  firefox上的设置
    - 浏览器全局代理配置：  
        首选项->高级->网络->连接设置
    - foxyproxy插件：  
        a) 新建代理服务器：（127.0.0.1，1080，sock5）  
        b) 更改工作模式：为全部URLs使用代理，此时就可以使用浏览器全局代理配置上网了  
        c) 模式订阅：  
        >
            订阅网址（https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt）
            备用网址（http://www.woodbunny.com/gfwlist.txt）
            更新频率：720
            Format：AutoProxy
            Obfuscation:Base64
            代理服务器：前一步配置好的代理服务器
        d) 结果：  
            在点击确定之后，如果没有问题的话，会很快就完成配置，超时或者“json解析失败”，
            那只能说这个订阅网址有问题或者无法订阅，具体问题见后面。
3.  chrome上配置
    - 浏览器全局代理配置:  
        高级-》网络-》更改代理服务器设置
    - Proxy SwichyOmega插件：  
        见：<https://github.com/FelisCatus/SwitchyOmega/wiki/GFWList>说明，这里不再描述

4.  错误问题
    - 模式订阅无法顺利的解析或者json解析失败：  
        更改网址，目前的订阅网址已经发生变化，见github上的说明
    - 浏览器代理服务器问题:  
        所有的网址访问都通过国外的代理服务器，即访问www.bilibili.com也通过代理进行访问，
        这种情况可能会碰到某些限制，所以采用到模式订阅。 


### 四，zshrc
> 这一块了解的不深入，我仅仅在会使用各阶段，具体cool的功能不太了解，后期会了解并写一个文章。

#### 4.1 安装
``` shell
    sudo aptitude install zsh
    sudo aptitude install curl
    sudo aptitude install git
```

#### 4.2 on-my-zsh
开源项目，为了配置zshrc而生，完全兼容bash，大大降低了zsh的使用门槛，
见<https://github.com/robbyrussell/oh-my-zsh>上的安装指南

#### 4.3 自定义配置
我的bash配置都是放在一个固定的文件中，在bash环境中是在.bashrc中进行导入的，同理
在zsh环境中，也可以通过在.zshrc中导入自定义的配置。

#### 4.4 shell和git
将你的shell配置放在云端，随时随地的进行部署和开发，其中shell脚本的几个原则：
-   密码/关键信息的分离  
    当你决定将你的配置进行分享或者在云端部署的时候就应该有这个原则（哎，被坑过），
    一般将这些数据配置为环境变量或者放在某一个单一的本地文件（不上传到云端），
    例如我的govpn脚本(<https://github.com/unlessbamboo/grocery-shop/blob/master/bamboo/local/bin/govpn>)：  
``` shell
    # 基础函数
    . /data/shell/base.sh
    # 导入vpn数据（账户/密码/端口等等信息）
    . /data/shell/vpn.sh
    # 其他命令和配置，从而根据命令行启动想要启动的代理 
    ...
```
-   自动化：  
    一直认为自动化是一个非常好玩的东西，当初学习python就是被这个快速/简单/自动化的pythonic
    给吸引的，当然那时候对shell也不了解（大学毕业时只会在vc++上编写NB的C:Hello world，醉了！）  
    操作过程：  
    >
            克隆git上的项目；  
            一键自动化部署你的bash配置以及其他相关;
            （目前还没完善，马丹，也是懒，抽点时间认真点搞一个类似在工作中的自动化部署脚本和自动化启动脚本）;
    操作例子：  
    > <https://github.com/unlessbamboo/grocery-shop/blob/master/bamboo/install.sh>

-   完善的日志记录
    >   我是一个笨蛋，我没有强大的逻辑思维，我不相信我自己，我只相信我的日志(~\_~)

### 五，tmux
> linux中一种管理窗口的终端分配软件（tmux,screen），用于替代终端模拟器（terminator等）

#### 5.0 效果图
![tmux效果图](http://obbuzq2fl.bkt.clouddn.com/ubuntu14/tmux%E6%95%88%E6%9E%9C.png)

#### 5.1 安装
关于tmux的介绍请自行了解原理，本文仅仅给出配置以及最后的效果，安装如下：
``` shell
    sudo apt-get update
    sudo apt-get install -y python-software-properties software-properties-common
    sudo add-apt-repository -y ppa:pi-rho/dev
    sudo apt-get update
    # 版本必须是最新的2.0.1
    sudo apt-get install -y tmux=2.0-1~ppa1~t
```

#### 5.2 配置
##### 5.2.1 基础配置
整个tmux的基础配置见<https://github.com/gpakosz/.tmux>上的说明。  
我从该项目上fork了一个版本库，并做了一些细微的注释和增项，从而更加适合我的工作习惯。
对于tmux的配置，了解的不多，后期有时间再深入了解。
``` shell
    mv .tmux .tmux.bak
    # 本人的个人项目，请更换该地址，里面更改了映射键等信息
    git clone https://github.com/Big-universe-group/.tmux.git
    cd ~
    ln -sf .tmux/.tmux.conf
    cp .tmux/.tmux.conf.local
```

<span id="p1234"></span>
##### 5.2.2 powerline配置
> 参考<http://askubuntu.com/questions/283908/how-can-i-install-and-use-powerline-plugin>最高答案
该项配置非常重要，牵涉的字体影响到vim和shell的配色等美观度。

##### 5.2.2.1 安装
-   安装Pip/git
``` shell
    sudo apt-get install python-pip git
    sudo pip install --upgreade pip
```
-   安装powerline
``` shell
    pip install --user git+git://github.com/Lokaltog/powerline
``` 默认情况下，powerline会安装在$HOME/.local/目录下，请在bash/zsh中配置PATH路径
``` shell
    PATH=$PATH:$HOME/.local/bin/
```
-   安装fonts字体
``` shell
    # 如果想要安装其他字体，请在<https://github.com/powerline/powerline>上下载其他相关
    wget https://github.com/Lokaltog/powerline/raw/develop/font/PowerlineSymbols.otf 
        https://github.com/Lokaltog/powerline/raw/develop/font/10-powerline-symbols.conf
    mkdir -p ~/.fonts/ && mv PowerlineSymbols.otf ~/.fonts/
    fc-cache -vf ~/.fonts
    mkdir -p ~/.config/fontconfig/conf.d/ && mv 10-powerline-symbols.conf ~/.config/fontconfig/conf.d/
```

##### 5.2.2.2 配置
-   vim配置
``` vim
    set rtp+=~/.local/lib/python2.7/site-packages/powerline/bindings/vim/
    " 添加新的字体，请更改为你系统中给已经存在的powerline字体
    set guifont=DejaVu\ Sans\ Mono\ for\ Powerline\ 9
    set laststatus=2
    " 保证xshell或者putty能够正常显示颜色
    set t_Co=256
    " 主题风格
    let g:Powerline_colorscheme='solarized256'
```
-   zshrc配置
``` shell
    # 在bash或者zsh中执行powerline配置文件
	# 正常方案
	#       export TERM="screen-256color"
	# 当前方案，vim和tmux配色方案的不兼容，导致的问题
	#   1，shell中不设置term方案
	#   2，将.tmux.conf文件中的default-terminal设置为 "xterm"
	#       alias tmux="TERM=screen-256color-bce tmux"
	#       或者
	#       alias tmux="tmux -2"
	. ~/.local/lib/python2.7/site-packages/powerline/bindings/zsh/powerline.zsh
	alias tmux="tmux -2"
```
具体配置见<https://github.com/unlessbamboo/grocery-shop/blob/master/bamboo/shell/.bamboo_profile>

- 	terminal终端上语言更改
执行完上述的配置后，可能会出现乱码现象，更改终端上的语言即可：  	
	配置文件首选项-》常规-》字体-》选择powerline	

### 六，后期
-	bamboo工作环境一键化安装（真正的一键化哦）
-	vim插件介绍和配置说明
-	tmux配置说明
-	zshrc配置说明
-   windows工作环境

### 七，参考
vim插件管理：<http://iamdatabase.blogspot.jp/2012/12/pathogen-git-vim.html>  
powerline: <http://askubuntu.com/questions/283908/how-can-i-install-and-use-powerline-plugin>  
其他参考这里不再一一考究了，本篇文章主要时总结印象笔记中的内容，不过很多知识都是来自因特网上。  
感谢这些人的分享，非常感谢。
