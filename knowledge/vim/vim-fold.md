---
title: fold语法的简要说明  
date:  2016-10-13 22:00:00  
tags: vim   
---

欢迎来到狂想的个人实验室。  
github：[unlessbamboo](https://github.com/unlessbamboo)


### 参考
vim中文文档<http://vimcdoc.sourceforge.net/doc/fold.html>


### foldmethod
#### 1，分类
manual      手动定义折叠
indent      一个缩进表示一个级别，更高的缩进表示更高的级别
expr        使用表达式来定义折叠
syntax      使用语法高亮来定义折叠
diff        folds for unchanged text
marker      folds defined by markers(标志) in the text


#### 2，fold-manual
##### 2.1 命令
:set foldmethod=manual

##### 2.2 使用
zf(Operator to create a fold)，通过组合移动命令
zF(Create a fold for [count] lines.)

###### 2.2.1 例子：
```
    zf70j           折叠光标之后的70行
    5zF             将当前行以及后面的4行折叠
    zfa(            折叠符号区域，其中a(为操作符待决模式中的motion，会在后面章节介绍
```

###### 2.2.2 save and load
:mkview             保存当前的折叠状态
:loadview           载入记忆中的折叠状态


#### 3，fold-indent
由缩进自动定义折叠；
```
foldlevel——由行的缩进处于'shiftwidth'计算得到;
foldnestmax——嵌套的最高级别
foldignore——空行或者foldignore中包含的字符开始的行会被忽略而归并到上一个或者下一个缩进级别中
```
##### 3.1 命令
:set foldmethod=indent
:set folelevel=1


#### 4，fold-expr
由折叠级别foldlevel来决定折叠，对每一行计算'foldexpr'来得到相应的折叠级别，暂时不用了解

#### 5，fold-syntax
由带有“fold”参数的语法项来定义折叠;
##### 5.1 命令
:set foldmethod=syntax

##### 5.2 例子
暂时没有


#### 6，fold-diff
该方法仅仅适用于当前窗口设定“diff”来显示不同之处时才有效

#### 7，fold-marker
在文本中加入折叠开始-折叠结束标志为来为你精确的定义折叠
zf和zd可以创建/删除一个用标志定义的折叠



### Fold command

#### 1，Create and delete folds
zf{motion} or {visual}zf        仅当foldmethod为(manual/maker)时有效
zF		Create a fold for [count] lines.  Works like "zf".
:{range}fo[ld]						*:fold* *:fo*
		Create a fold for the lines in {range}.  Works like "zf".

zd      删除光标下的折叠        仅当foldmethod为(manual/marker)时有效
zD		Delete folds recursively at the cursor.

zE      Eliminate(除去)窗口中的所有folds


#### 2，Open and close folds
zo      打开光标下的折叠。在可视模式下，所选区域折叠被打开一个级别
zO      Open all folds under currsor recursively.

zc      关闭光标下的折叠（即zo的反向操作，折叠操作）。在可视模式下，
        所选区域内的所有行的折叠都关闭一级
        PS：该操作仅仅作用于当前行，不会改变foldlevel，所以和zr不可以
            搭配使用哦
zC		Close all folds under the cursor recursively.

zm      折叠更多（作用于整个文件），将foldlevel直接减一，即将最高级别
        的代码折叠，例如：set foldlevel为4，则第一次会着地level=4的代码，
        以此类推
zM		Close all folds: set 'foldlevel' to 0.

zr      减少折叠（作用于整个文件），将foldlevel直接加1，见zm命令
zR		Open all folds.  This sets 'foldlevel' to highest fold level.

zn      不折叠，复位foldenable，所有折叠都打开，但是foldlevel不发生任何变化
zN		Fold normal: set 'foldenable'.  All folds will be as they
		were before. zn的方向操作
zi      zn/zN的逆向操作

#### 3，Moving over folds
[z      在open fold的开始位置哦，这个有点类似{}的跳转，在python中蛮好用的
]z      在open fold的结尾位置

zj      到下一个折叠的开始处，所以流程：level1->level2->level3->...，然后下一个
zk      到上一个折叠的结尾处
