---
title: vim术语
date:  2016-10-13 22:00:00  
tags: vim   
---

欢迎来到狂想的个人实验室。  
github：[unlessbamboo](https://github.com/unlessbamboo)


### 1 quickfix和location
#### 1.1 quickfix
quickfix list中记录vim编译过程中出现错误的一个list windows.
#### 1.2 localtion
location list中见记录各种file位置信息的一个list windows，一个窗口对应一个list
#### 1.3 关系
quickfix和locaotion的命令相似，仅仅是首字母不一样，quickfix(c)，location(l)
``` bash
    # 列出
    :clist
    # 跳转到对应的编号上
    :cc {n}
    # 下一个或者上一个
    cn/cp
```
#### 1.4 附加
注意quickfix/location和buffer list的不同之处哦 


### 2 motion
#### 2.1 jumps and jumplist
##### 2.1.1 jumps
Print the jump list.
``` vim
    :ju 显示jumplist信息
```
##### 2.1.2 jumplist
Jumps are recommbered in a jump list.
With Ctrl-O and Ctrl-I command you can go to cursor positions before olds jumps,
and back agagin.
``` vim
    Ctrl-O      回退到上一个jumps
    Ctrl-I      进入到下一个jumps，首先当前jumps position不是最后一个哦
```
#### 2.2 tags/link
如果使用tags和cscope来进行跳转（link/tags）则使用Ctrl-]，Ctrl-T来进行
``` vim
    Ctrl-]      go to link or tags
    Ctrl-T      Go back
```


### 3 undo
#### 3.1 undo
```
    undo/u          undo one change.
    u [num]         Jump to after change number [num].

    U               Undo all latest change on one line.
```
#### 3.2 redo
```
    redo/Ctrl-R     Redo [count] change which were undone.
```
#### 3.3 undobranchs
##### 3.3.1 undolist
List the leafs in the tree of changes.
##### 3.3.2 goto undo
所有一下的前提就是必须存在一个队列(list)，以便进行定位操作，缓冲区哦。
功能：进入某一个文件状态点
```
g-			            Go to older text state. 
*:ea* *:earlier*
    :earlier {count}	Go to older text state {count} times.
    :earlier {N}s		Go to older text state about {N} seconds before.
    :earlier {N}m		Go to older text state about {N} minutes before.
    :earlier {N}h		Go to older text state about {N} hours before.
    :earlier {N}d		Go to older text state about {N} days before.
    
    :earlier {N}f		Go to older text state {N} file writes before.

*g+*
    g+			        Go to newer text state.

*:lat* *:later*
    :later {count}		Go to newer text state {count} times.
    :later {N}s		    Go to newer text state about {N} seconds later.
    :later {N}m		    Go to newer text state about {N} minutes later.
    :later {N}h		    Go to newer text state about {N} hours later.
    :later {N}d		    Go to newer text state about {N} days later.
    
    :later {N}f		    Go to newer text state {N} file writes later.
```
