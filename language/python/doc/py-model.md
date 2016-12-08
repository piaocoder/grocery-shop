----
title: 模块导入
date: 2016-08-06 12:00:00
tags: python
----
欢迎来到狂想的个人实验室。  
github：[unlessbamboo](https://github.com/unlessbamboo)
更新：2016年 08月 12日 星期五 23:33:07 CST


### 一 Introduction
#### 1.1 使用环境
世界那般大，你居然叫我只呆在这里发呆？

#### 1.2 文章知识点
1. 模块导入原理
2. 循环导入


### 二 模块导入
> 主人去天外宇宙旅游了，有空再写。


### 三 循环依赖
> 之前在豆瓣上看过一个循环依赖的说法（from 和 import）的机制不一样，
可能是那时候理解错误了，而且对循环依赖的理解也不是非常深入，所以产生该测试用例。

测试循环依赖在import A.a和from A import a这两种不同的语句中的
副作用。
#### 3.0 代码所在
<https://github.com/unlessbamboo/grocery-shop/tree/master/language/python/src/model>

#### 3.1 import A
> 下面讲的其实不像循环依赖

测试代码rely\_client.py和rely\_server.py。  
##### 3.1.1 导入循环的原因：  
- rely\_server中导入rely\_client；  
- 但是rely\_client在一开头又开始导入rely\_server；
- 在新的server代码执行时发现client已经导入，继续执行，直到语句：  
    rely_client.clientTest()，但是其实该函数目前还未导入，所以发生错误。

##### 3.1.2 解决办法：
见rely\_server\_solve.py和rely\_client\_solve.py文件
##### 3.1.3 副作用：
某一个语句会被执行两遍

#### 3.2 from A import a
测试代码rely\_client\_from.py和rely\_server\_from.py
> 该例子并未像1.1中进行某些对象的实例化或者对象执行
##### 3.2.1 原因
类似1.1中的例子，只不过现在将“冲突点”提前放在了import语句。
> 想想这里面的共同之处，所以依赖不分from和import的差别，
关键是“冲突点”

#### 3.3 解决思路
- 将冲突点import放在文件末尾，但是该用法一般在极度模块化的代码结构中才可能，例如flask中的蓝本
- 延时导入，局部导入import，但是可能会有代码执行时的延迟现象哦
- 良好的代码组织结构（爱，哎，唉...）
