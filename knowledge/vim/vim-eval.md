---
title: Eval变量相关说明  
date:  2016-10-12 21:00:00  
tags: vim   
---

欢迎来到狂想的个人实验室。  
github：[unlessbamboo](https://github.com/unlessbamboo)


### 参考
eval<http://vimcdoc.sourceforge.net/doc/eval.html>  
variable<http://vimcdoc.sourceforge.net/doc/eval.html#internal-variables>
PS:以下表达式相关，都默认调用eval



### 变量
#### 1,类型和作用域
类型
```
    数值            32位或者64位符号整数
    浮点数
    字符串          “xxx", 'xxxx xx'
    函数引用        就是函数调用
    列表            有序列表,[1,2]
    字典            关联无序数组，{'bamboo':3, 'kuang':'aa'}
```
作用域
``` vim
    b:              局部于当前缓冲区
    w:              局部于当前窗口
    t:              局部于当前标签页
    g:              全局
    l:              局部于函数
    s:              局部于vim脚本
    a:              函数参数
    v:              vim预定义的全局变量
```


#### 2,函数
let Fn = function("MyBamboo")
let fn = string(Fn)
let r = call(Fn, arguList)


#### 3,list
```
    let ml = [1, two, 3, 'four']

    let mlitem = ml[0]
    let mlitem2 = get(ml, 1)

    let ml2 = ml + [4,5]

    let subml = ml[1:3]

    let ml3 = ml
    if ml3 is ml
        echo "Var ml3 is equal to Var ml"
    else
        echo "xxxxx"
    endif

    
    let [var1, var2, var3, var4] = ml
    let [var1; ml4] = ml
```


#### 4,dict
``` vim
    let d1 = {'bamboo': 3, 'kuang':'xxx'}
    let d1['bamboo'] = 4

    for key in keys(d1)
        echo key. ':' . d1[key]
    endfor

    " 字典函数
    "       self引用函数所在的字典
    function Mylen() dict
        return len(self.data)
    endfuncion
    let myD = {‘data': [0, 1], 'len': function('Mylen')}
    echo myD.len()
```


### 表达式
#### 1,基本小结
``` vim
    " if-then-else
    expr1 ? expr2 : expr3

    " 逻辑/算术
    expr1 && expr3

    expr1 == expr2 
    expr1 ==? expr3 忽略大小写
    expr1 ==# expr3 匹配大小写

    expr1 + expr2   数值加法或者list连接
    expr1 - expr2   数值减法
    expr1 . expr2   字符串连接

    !expr1

    exrp2[expr1:expr2]
    expr2[expr1]
    expr3(expr1, ...)   函数调用

    &options            选项值
    (expr1)             嵌套表达式
    variable            内部变量
    $VAR                环境变量
    @r                  寄存器变量
```

### 函数
#### 1,内建函数
内建函数<http://vimcdoc.sourceforge.net/doc/eval.html>

#### 2,自定义函数
##### 2.1 获取函数
``` vim
    fu[nction]          列出所有函数以及参数
    fu {name}
    fu  /{pat}
```

##### 2.2 定义函数
###### 2.2.1 首行
``` vim
    格式：fu[!] {name}([arguments]) [range] [abort] [dict]
```

###### 2.2.2 结束函数定义
``` vim
    endf[untion]，必须单起一行
```

###### 2.2.3 删除函数
``` vim
    delf[untion] {name}
```

###### 2.2.4 从函数返回
``` vim
    retu[rn] [expr]    返回 
```


##### 2.3 例子
``` vim
    function Compute(n1, n2)
      if a:n2 == 0
        return ["fail", 0]
      endif
      return ["ok", a:n1 / a:n2]
    endfunction

	let [success, div] = Compute(102, 6)
	if success == "ok"
        echo div
    endif
```


#### 3,自动载入函数
在需要func的时候才自动的提供函数定义，方法有：  
    自动命令  
    runtimepath里的autoload目录

##### 3.1 自动命令
``` vim
    " 载入文件中的所有函数（BufNet开头）
    autocmd FuncUndefined BufNet* source ~/vim/bufnetfunc.vim
```


##### 3.2 autoload脚本
``` vim
    " 使用call调用指定文件中的函数名
        call function1#func1()
    " 此时如果function1->func1没有载入内存中，vim在runtimepath
    " 的autoload目录里面搜索文件名-function1，一般为：
    "   ~/.vim/autoload/function1.vim
    " 并寻找函数func1
        function function1#func1()
            echo "Done.."
        endfunction
```
