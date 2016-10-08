---
GCC知识
---


### 1 Introduction
#### 1.1 Abstract(简介)
GCC-GNU Compiler Collection
- 编译程序组成
- GCC部件组成

#### 1.2 Command-line Options
命令行选项格式

#### 1.3 C编译
- 预处理（C++向后兼容）
- 编译过程
- C语言扩展

#### 1.4 C++编译
- 编译过程
- C++语言扩展

#### 1.5 Localization
GCC的本地化设置，i18n(internationalization, i18个字母n）

#### 1.6 Link
链接，请结合《程序员自我修养-链接、装载与库》一书


### 2 Abstract
> GCC是GUN项目的一个产品
#### 2.1 编译构成
前端--读取程序源码--以树形式存储到memory-resident table中。  
后端--读取树--转换为汇编语言
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


### 4 C编译
#### 4.1 GCC由来
早起的UNIX上C编译程序叫做CC（C Compiler），所以GUN最早的编译程序
成为GCC。

#### 4.2 编译过程
#### 4.2.1 预处理
选项：-E  
文件格式：a.i  
例子：
> gcc -E helloworld.c -o helloworld.i

#### 4.2.2 汇编
选项：-S  
文件格式：a.s  
例子：
> gcc -S 
