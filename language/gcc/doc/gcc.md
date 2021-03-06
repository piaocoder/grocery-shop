---
title: gcc基础
date:  2016-09-25 23:00:00  
tags: c  
---


### 1 Introduction
#### 1.1 Abstract(简介)
GCC-GNU Compiler Collection  
- 编译程序组成
- GCC部件组成   

#### 1.2 Command-line Options
命令行选项格式
#### 1.3 Compile
> 请结合《程序员自我修养-链接、装载与库》和《GCC技术参考大全》  

#### 1.4 C编译
- 预处理（C++向后兼容）
- 编译过程
- C语言扩展  

#### 1.5 C++编译
- 编译过程
- C++语言扩展  

#### 1.6 Link
> 请结合《程序员自我修养-链接、装载与库》和《GCC技术参考大全》  

#### 1.7 Localization
GCC的本地化设置，i18n(internationalization, i18个字母n）


### 2 Abstract
> GCC是GUN项目的一个产品  

#### 2.1 编译构成
前端--读取程序源码--以树形式存储到memory-resident table中。  
后端--读取中间语言--转换为汇编语言
##### 2.1.1 前端
- 词法分析
- 语法分析
- 伪汇编语言，Register Transfer Language  

##### 2.1.2 后端
- 获取RTL，删除冗余信息
- 汇编语言
- 目标文件

#### 2.2 组成部件
#### 2.2.1 安装部分
- gcc
- g++/c++，gcc的一个版本，默认语言c++
- ccl/cclplus，实际上的C/C++编译程序
- configure--脚本，用于设置配置值和创建make的描述文件
- libgcc/libstdc++，标准库
- ...  

#### 2.2.2 软件工具
> binutils包/gcc包

- AR，创建和管理目标库文档
- AS，GUN汇编器
- autoconf，产生shell脚本去自动的配置源代码包来编译
- gdb 调试
- ld 连接
- nm列出目标文件中的符号
- objdump显示目标文件中保存的信息
- readelf从ELF格式的目标文件中显示信息  


### 3 Command-line Options
#### 3.1 格式
gcc [选项] [选项值]

#### 3.2 分类
- 指定语言，例如-c99
- 指定平台或者操作系统
- 其他通用选项  


### 4 Compile
> 编译器--将高级语言翻译为机器语言的一个工具  

#### 4.1 Compilation Process
源代码-->(扫描器/词法分析)  -->记号(Tokens)
      -->(语法分析)         -->语法树
      -->(语义分析)         -->标示语义后的语法树
      -->(代码优化)         -->中间语言树
      -->(代码生成器)       -->目标代码
      -->(目标代码优化)     -->最终优化后的目标代码
#### 4.2 词法分析
Lexical Analysis。  
工具Lex--按照语法规则生成tokens;  
Scanner逐字符的扫描，将一个个的标识符、关键字、字面量等等信息
变为一定格式的二元组（<单词种类，单词的属性值>）。  
参考编译原理中的Finite State Machine（有限状态机）。
#### 4.3 语法分析
Grammar Parser.  
工具YACC--按照语义规则对输入token进行解析，构建语法树
仅仅简单的关注表达式的语法层面，不会深究该表达式是否合法。  

Parser采用上下文无关语法（指定规则，栈结构）扫描上面的所有Token，
生成一个简陋的语法树（一个以表达式为节点的树）。
#### 4.4 语义分析
Semantic Analysis.  
静态语义分析，动态语义分析仅仅在运行时才可以解决。  

Static Semantic包括对声明/类型的匹配、转换等等，最终形成一个
标示语义后的语法树。
#### 4.5 代码优化
Source Code Optimizer.  
对语法树进行优化，将语法树转变为中间语言，从而进入后端的处理。  
中间语言常见以三地址码的形式（< x= y op z > ）存在。 
参考2.1中的说明，中间语言使得整个处理逻辑分为前后端。
#### 4.6 代码生成和优化
Code Generate.  
对中间语言处理，生成目标代码，即机器语言。
对目标代码进行优化，生成最终的目标代码。  


### 5 C编译
#### 5.1 GCC由来
早起的UNIX上C编译程序叫做CC（C Compiler），所以GUN最早的编译程序
成为GCC。

#### 5.2 编译过程
##### 5.2.1 预处理
选项：-E  
文件格式：a.i  
例子：
> gcc -E helloworld.c -o helloworld.i  

##### 5.2.2 生成汇编（Assembly）
选项：-S  
文件格式：a.s  
例子：
> gcc -S helloworld.i -o helloworld.s  

##### 5.2.3 编译
> -c选项其实可以跳过预处理和生成汇编过程  

选项：-c 
文件格式：a.o
例子：
> 
    gcc -c helloworld.s -o helloworld.o
    gcc -c helloworld.c -o helloworld.o

#### 5.3 C语言扩展
> 编译器或者编译套件额外提供的功能，并非原有的C功能，但是以前
的扩展也慢慢变为新的标准，万事万物总是在变化的。  

##### 5.3.1 对齐
boundary alignment对齐，返回指定数据项的对齐值
##### 5.3.2 零长度数组
> 注意，变长数组是动态数组，和零长度数组是不一样的。
> 参考<GCC>61页，<C PLUS>274页  

###### 5.3.2.1 例子
```gcc
    struct {
        int     num;
        char    str[0];
    }test, test1;
```
###### 5.3.2.2 原理
利用编译器来实现，使用test->str时，指针就是表示分配内存地址的
某块buffer。数组的原地就是内容，指针保存的内容的地址。
PS: 两者的汇编代码也不同

##### 5.2.3 属性（Important）
关键字：__attribute__
功能：为函数和数据声明赋属性值信息，从而让编译器有目的的优化代码
分类：声明函数的属性、声明变量的属性、声明数据类型的属性
参考：《GCC技术参考大全》65页
例子：
```gcc
    // 不返回
    void display() __attribute__((noreturn)) {}; 
```

##### 5.2.4 inline
内嵌函数

##### 5.2.5 复合语句或者表达式
```gcc
    int rst = ({
        int a = 5;
        int b;
        b = a + 3;
        });
    // 最终的结果为8
```

##### 5.2.6 函数嵌套（inner）
内部函数/内部类

##### 5.2.7 变长数组(VLA)
###### 5.2.7.1 使用
C99标准的新特性，函数定义列表中的变长数组实际上并没有创建或者
值传递数组，VLA实际上是一个指针
```
   // 正确用法
   int sum(int rows, int cols, int arr[rows][cols]);
   int sum(int, int, int arr[*][*]);

   // 错误用法
   int sum(int arr[rows][cols], int, int);
```
###### 5.2.7.2 区别
VLA和动态内存分配的区别，前者会自动释放内存，见《C PLUS》344页

##### 5.2.8 Others
typedef/Macros概念等等


### 6 C++编译
#### 6.1 编译过程
##### 6.1.1 预处理
选项：-E
文件格式：a.ii
例子：
> gcc -E helloworld.cpp -o helloworld.ii  

##### 6.1.2 生成汇编
选项：-S
文件格式：a.s
例子：
> gcc -S helloworld.ii -o helloworld.s  

##### 6.1.3 编译
选项：-c
文件格式：-o
例子：
> gcc -c helloworld.s -o helloworld.o


### 7 Link
> Link的本质就是将各个模块化之间相互引用的部分处理好，使得模块
之间能够正确的衔接。  

#### 7.1 链接过程
```
Address and Storage Allocation   
           ||  
    Synbol Resolution  
           ||   
        Relocation
```
- 空间和地址分配：扫描所有目标文件，收集长度、属性等，建立映射关系 
- 符号解析：对程序中每一个符号（标识符等）解析
- 重定位：对一些符号地址的修正过程  

#### 7.2 静态链接
##### 7.2.1 如何合并目标文件？
###### 7.2.1.1 方法
- 按序叠加-不同的目标文件按顺序堆积
- 相似段合并-相同性质的段合并到一起  

###### 7.2.1.2 Two-pass Linking
- 空间和地址分配--确定符号地址
- 符号解析
- 重定位  

##### 7.2.2 如何确定符号地址？
扫描提取所有符号信息，计算偏移量，设置VMA地址信息，更新全局
符号表中的符号地址信息。
##### 7.2.3 什么是符号解析？
对目标文件中的所有符号进行重新识别的过程，目标文件的符号详见
《Linking》ELF文件格式一章。  
解析过程就是根据符号类别去查找符号表中的对应符号信息，之后调用
重定位来进行地址信息的更新。
##### 7.2.4 重定位？
描述如何修改相应端的信息的过程，每一个端都有一个重定位表存在。
##### 7.2.5 静态链接过程
> 静态库是一组目标文件的集合

ld通过链接脚本，去确定：目标文件集、库文件集、是否保留调试信息、
输出文件格式等等信息，最终生成库文件。
#### 7.3 动态链接
> 把Linking过程推迟到运行过程再进行，虽然会造成一些性能消耗

##### 7.3.1 产生原由？
- 随着软件库增加，公用软件库的重复包含，造成磁盘空间和内存的巨大消耗
- 不同软件库之间因为版本更换不统一，导致开发和发布的不便  

##### 7.3.2 优缺点
###### 7.3.2.1 优点
- 减少空间消耗
- 增加程序可扩展性和兼容性  

###### 7.3.2.2 缺点
- 性能
- 接口因为版本管理机制的混乱，可能导致兼容性出现问题  

##### 7.3.3 如何合并目标文件？
采用延迟绑定，合并方式同静态链接
##### 7.3.4 如何确定符号地址？
###### 7.3.4.1  方法
- 固定装载地址
- 装载时重定位  

##### 7.3.5 动态符号表和动态重定位表
参见静态链接的符号表和重定位表，具体过程见《Linking》207页
##### 7.3.6 动态链接过程
- 动态连接器自举
- ld装载共享对象
- 重定位
- 初始化  


### 8 Localization
```
    Internationalization：程序的多语言能力
    Locationation：一种操作，内置程序，用户可读和其他语言的转换。
    Native Language Support：用于指定国际化和本地化的所有操作
    i18n：国际化，i + 18字母 + n
    l10n：本地化
```
#### 8.1 本地化类别
```
    LC_ALL          所有成员
    LC_ADDRESS      地址、邮政编码等等
    LC_NAME         人名规范
    ...
```
#### 8.2 本地化编写
po文件和mo文件，python中做过，后续跟进。
