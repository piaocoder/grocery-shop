---
Autocmd文档
---


### 参考
命令：autocmd命令<http://vimcdoc.sourceforge.net/doc/usr_40.html#40.3>
详细说明：help autocmd或者<http://vimcdoc.sourceforge.net/doc/autocmd.html>


### 基本使用-命令格式以及介绍
autocmd——自动命令，当某些事件发生时（文件读入/改变缓冲区,etc），此类自动
命令会被自动的执行；

#### 1，命令格式
autocmd [group] {events} {pat} [nested]  {command}
    group               可选项，管理和调用命令
    events              触发事件列表，用逗号隔开
    pat                 文件命令，通常伴随通配符，目标文件类型
    nested              允许自动命令的嵌套使用
    command             欲被执行的命令


#### 2, 事件
各种具体的操作触发事项；
见<http://vimcdoc.sourceforge.net/doc/autocmd.html>说明

##### 2.1 文件读入
BufReadPost         文件被调入编辑之后触发，常常用来设定某些选项
例如，为.gsm设置filetype:
    autocmd BufReadPost *.gsm set filetype=gsm
其中BufReadPost为events，\*.gsm为filePattern，set filetype=gsm为cmd

##### 2.2 文件类型
FileType            当某一类型的文件读入前，做一些准备工作
例如，读取text文件类型时，调入一组缩写
    autocmd FileType text source ~/.vim/abbrev.vim
例如，编辑文件前，插入vim模板
    autocmd BuffNewFile \*.[ch]  Oread ~/skeletons/skel.c


#### 3,匹配模式
类似shell的模糊匹配


#### 4,组
定义分组之后，所有的自动命令都会自动在内存中被重新分组，从而高效的
对某一个分组进行操作（删除等）
例如：
``` vim
        :augroup cprograms
        :  autocmd BufReadPost *.c,*.h :set sw=4 sts=4
        :  autocmd BufReadPost *.cpp   :set sw=3 sts=3
        :augroup END
	等价于
        :autocmd cprograms BufReadPost *.c,*.h :set sw=4 sts=4
        :autocmd cprograms BufReadPost *.cpp   :set sw=3 sts=3
```


#### 5,嵌套
一般而言，一个事件触发的自动命令执行之后，便不会再次触发其他事件，
这是不利的，所以产生nested
例如：
``` vim
	autocmd FileChangedShell * nested edit 
```

#### 6,cmd
普通“命令行”命令或者“执行自动命令”
##### 6.1 cmd中的特殊字符
具体见<http://vimcdoc.sourceforge.net/doc/cmdline.html#:%3Cafile%3E>说明  
在某些期待文件的命令里面可以使用<afile>等来进行一些其他操作


### 基本使用-附加命令

#### 1,删除自动命令（autocmd!）
如果要删除某一个命令，则定义一模一样的命令，但是删除{command}字段
例如：
``` vim
	autocmd! FileWritePre *
```

#### 2,自动命令列表
列出当前定义的所有自动命令，格式有点类似delete操作，但是没有！
例如：
``` vim
	" 列出所有命令
	autocmd
	" 列出某一个事件的所有命令
    autocmd BufNewFile
    " 列出所有事件的文件模式为*.c
    autocmd * *.c
    " 列出组内所有命令
    autocmd groupname
```

#### 3,忽略事件
忽略事件列表中所有事件的触发
``` vim
    " 事件列表
    set eventignore=WinEnter,WinLeave
    " 所有事件
    set eventignore=all
    " 恢复正常（清空事件忽略）
    set eventinnore=
```


### 执行自动命令
Vim可以非自动的执行自动命令。

#### 1,执行自动命令
在事件触发后执行一个自动命令
##### 1.1 do[autocmd]
###### 1.1.1 格式
```
    doautocmd [nomodeline] [group] {event} [fname]
    
    fname       默认为当前文件或者针对当前缓冲区
    group       特定组或者所有组
    nomodeline  应用完自动命令后，该选项用于过滤否则自动命令中的设置
```

###### 1.1.2 嵌套包含到自动命令au中
au BufEnter \*.cpp duau BufEnter x.c
避免死循环

##### 1.2 doautoa[ll]
为每个载入的缓冲区应用自动命令。用于执行类似于设置选项/修改高亮等任务
的自动命令。

#### 2,使用普通模式命令
即自动命令执行“命令行”命令
``` vim
    " 读取.log命令之后移动光标到末尾
    autocmd BufReadPost *.log normal G
```
