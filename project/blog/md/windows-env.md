---
title: windows下工作环境配置  
date: 2016-08-03 12:00:00
tags: 工作环境
---

欢迎来到狂想的个人实验室。  
github：[unlessbamboo](https://github.com/unlessbamboo)  
update time： 2016年 08月 12日 星期五 23:38:01 CST

## 一，Introduction
### 1.1 使用环境
windows7, windows10

### 1.2 文章知识点
1.  quickly start
2.  editor
3.  python
4.  git/TortoiseGit
5.  browser
6.  terminal
7.  office
8.  Windows shortcut keys

## 二，quickly start
> 快速启动，快速搜索，任务栏增强工具

### 2.1 Launchy
> 我待你如初恋，你依待我如初恋，奈何奈何，哎(Listary).

#### 2.1.1 安装
下载：<https://www.launchy.net/>
安装：click-click-\*

#### 2.1.2 使用
皮肤：Select what you like.
添加扫描目录和新增新的文件类型：例如D盘，见选项->目录
重建索引数据库：更新数据库

#### 2.1.3 截图
啊啊啊啊啊


### 2.2 Bins
> 一款非常棒的增强windows任务栏的插件
##### 2.2.1 安装
支持系统：win7/win8/win10
下载：付费的，可以跳到2.3小节不适用该软件
安装：click-click-click
 
##### 2.2.2 功能
-   分类：将同一功能的快捷方式归类，其中每一类有主次之分
-   Stronger：增加任务栏上的快捷方式，然后可以隐藏桌面图标，嘿嘿
-   快速进入指定目录：通过将指定目录的快捷方式放置在任务栏中，
    实现快速打开文件夹，不过相比listary，弱爆了（还要自己制作ICON）

##### 2.2.3 效果图
啊啊啊啊


### 2.3 Listary
> 实现快速搜索定位（命令/路径/执行程序），从而快速的打开文件夹等

#### 2.3.1 原理
使用与Everything相似的原理，通过遍历USN jounal更新索引，可以实现秒级的索引建立和搜索反馈(NTFS文件系统）。

### 2.3.2 设置
-   快捷键：选项中设置启动快捷键
-   外观/索引等   

### 2.3.3 基础用法
快捷键：工具条快捷键(选项中设置），搜索命令/路径/程序，执行智能匹配
功能：快速的查找目标，之后利用Enter以及其他按键就可以启动应用后者进入目标所在的文件夹

### 2.3.4 收藏夹
快捷键：在某一个目标文件夹，双击-添加收藏夹即可
功能：就相当于win10上的快速访问，browser上的书签

### 2.3.5 历史记录
功能：快速的浏览过去的搜索记录


## 三，editor
> 真不习惯在windows上使用gvim(v\_v)

### 3.1 Notepad++
啥都不说

### 3.2 gvim
安装后还得安装一大堆适合windows上的插件，哎，用的不多


## 四，python
> windows上开发python仅仅用过一次，帮老同学在windows上搭了一个django环境并进行基本的socket通信中间代理，之后没有再搞过，所以用的不多。
### 4.1 安装
下载python-3.5.2.exe，是时候全面拥抱python3，啊，新时代。

### 4.2 插件
完全安装python安装包之后，一般都会自动安装pip和自动设置python路径，所以直接使用pip安装即可

### 4.3 卸载
请勿暴力卸载python，不然你会碰到灾难性的烦恼的（还得先安装同一版本，然后再卸载，醉了）

## 五，git/TortoiseGit
> 海龟果然是版本控制GUI专业户

### 5.1 git
#### 5.1.1 安装
安装时选择full方式，安装所有插件，并非custom，之后可以通过git自带的shell命令行进行各项设置

#### 5.1.2 配置
用户名和邮箱：
``` bash
    git config --global user.name "unlessbamboo"
    git config --global user.email "unlessbamboo@gmail.com"
```
公钥：
``` bash
    # 生成公钥或者自己拷贝.ssh目录到C:\Users\用户名\下
    mkdir ~/.ssh
    ssh-keygen -t rsa -c "unlessbamboo@gmail.com"
    ssh -T git@github.com
```
git 操作：
``` bash
    # 见<git操作纪要>
    git fetch
```

### 5.2 tortoisegit
#### 5.2.1 安装
-   说明：tgit或者海龟git，另外有一个tortoiseSVN....
-   安装：下载安装

#### 5.2.2 配置
> 居然和rsa的公钥不兼容，什么鬼？
生成公钥：
    >
        运行Puttygen程序
        点击generate生成key，移动鼠标加快生成速度（我的错觉吗？）
        设置访问密码；
        保存rsa的公钥和私钥，在之后clone时使用，以后跨机器使用，最后存储在.ssh下，一起嘛
        复制公钥到github.com上

更改tortoiseGit的ssh可执行程序路径：
    setting->network->SSH client中替换为：git-install-path\Git\user\bin\ssh.exe

#### 5.2.3 使用
各种图形化操作


## 六，browser
参考ubuntu上的browser，大体相同：<http://www.unusebamboo.com/2016/08/03/ubuntu14-04-env/>

## 七，terminal
### 7.1 xshell
> 远程连接的不错选择，因为我第一次接触就是这个，所以其他putty以及cmder都没用过
#### 7.1.1 安装
安装xshell5或者xshell4

#### 7.1.2 公钥
生成xshell独有的公钥私钥

#### 7.1.3 配色方案
网上搜索或者自己配置一份适用的配色方案，之后导入即可


### 7.2 PowerShell
> 至少比cmd用着好点吧
待补充，其实windows上面的命令行用的真不多，windows上的开发也就大学的搞过一点点。
大学四年用windows都用到狗身上去了，哈哈


## 八，office
> word/visio/powerpoint，本人写文档必备，大学四年可能就学到这点东西了(~\_~)
具体见后续的《office适用纪要》


## 九，windows shortcuts keys
### 9.1 小娜小娜
>
    wins + c 语音搜索
    wins + s 文字搜索
    
    wins + R 打开运行对话框

### 9.2 窗口设置
>
    多任务窗口：wins + tab
    贴靠窗口： wins + 上下左右

    创建虚拟桌面： wins + ctrl + d
    关闭虚拟桌面： wins + ctrl + F4
    切换虚拟桌面： wins + ctrl + 左右

### 9.3 系统应用快捷键
>
    wins + x + 按键
    # 设备管理/磁盘管理/程序和功能/任务管理器/控制面板

### 9.4 系统管理
    快速关机： Alt + F4
    设置栏：wins + I，设置各项系统基本配置
    关闭开机启动：msconfig->启动-》禁用
    添加开机启动：msconfig->shell:startup->复制lnk

## 十，未来工作
1，添加截图
2，office说明
