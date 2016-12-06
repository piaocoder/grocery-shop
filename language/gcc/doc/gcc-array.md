---
title: 数组以及数组实参  
date: 2016-09-01 21:00:00  
tags: c
---

欢迎来到狂想的个人实验室。  
github：[unlessbamboo](https://github.com/unlessbamboo)


### Introduction
- 数组参数
- 多重数组和指针
- 指针


### 1, 数组参数
> 
    数组，特别时多维数组，在作为参数（形参/实参）时会碰到一些问题，
    尤其是和指针之间的转换发生时。

#### 1.1 问题
一维数组——虽然下面的两者传递的都是一个地址信息，但是需了解区别：
```gcc
    int func1(struct Node *root)
    {
        ...
    }
    
    struct Node array[100] = {...};
    struct Node node;

    // 传递一个结构体数组
    ret = func1(array);

    // 传递一个节点指针
    ret = func1(&node);
```

二维数组——注意和一维的区别：
```gcc
    int func2(int **arr)
    {
        ...
    }

    int array[2][2] = {...};
    // Warning: int[][]自动转为int (*)[2]，但是和形参int **不匹配
    ret = func2(array);
```
此时编译会产生警告信息，如果强制使用可能会出现Segmentation fault，因为
\*array的范围不确定，如果在func2中访问一维数组的第三个元素会造成越界访问
错误。


#### 1.2 数组参数枚举
> 下面讲解的所有多维数组操作都以二维数组为例
##### 1.2.1 一维
一维数组无需过多的在意，一维其操作类似指针，除了指针常量以外没有其他区别
```gcc
    // 如下四个函数声明对一维数组都是适用的
    int func1(int *array);
    int func2(int array[3]);
    int func3(const int array[3]);
    int func4(int array[], int m);
```

##### 1.2.2 二维
整个数组值传递：
```gcc
    int array[m][n];
    int func1(int arr[m][n]);
    int func2(int arr[][n], int m);

    // 上面两个函数对应的实参可以有：
    func1(array);
    
    int (*p)[n] = array;
    func1(p, m);
```

数组指针（推荐方式）
```gcc
    int array[m][n];
    int func1(int (*arr)[n], int m);

    // 可以调用的实参，该方式相比上面的func2，不是值传递
    func1(array, m);

    int (*p)[n] = array;
    func1(p, m);
```

一维指针：
> 用一维数组的方式来处理多维数组，其中内存为连续的
```gcc
    int func1(int *ptr, int m, int n);
    
    // 实参调用

    int *array2 = (int*)malloc(m*n*sizeof(int));
    func1(array2, m, n);

    int array[m][n];
    func1(array[0], m, n);
    func1((int*)array, m, n);
    func1((int*)&array[0][0], m, n);
```

二维指针：
```gcc
    int func1(int **arr, int m, int n);

    // 注意，仅仅分配了(int*)类型
    int **ptr = (int **)malloc(m*sizeof(int*));
    for (i=0; i<m; i++) {
        ptr[i] = (int*)malloc(n*sizeof(int));
    }
    func1(ptr, m, n);

    // 当然，实参也可以时二维数组，但注意边界
    int array[m][n];
    func1((int**)array, m, n); 
```


### 2 多重数组和指针
#### 2.1 转化例子
> 数组是一个特定类型的固定指针
```gcc
    int **p = NULL, **p2 = NULL;
    int array[3][3] = {{0}};

    p = (int**)array;
```
其中P作为双重指针，存放的array的首地址，可以分解为：
```gcc
    // 1 地址拷贝
    p = array;

    // 2 类型
    (int **)p;

    // 3 段错误
    **p = 3;
```

#### 2.2 分析
##### 2.2.1 二级指针
- 本质上为一个指针，一个内存地址
- 不过指针中存放的另外一个指针的地址，编译器区别对待而已；
> Any problem in computer science can be solved by another layer of indirection.

##### 2.2.2 分析
###### 2.2.2.1 正常情况
双重指针使用场景应该是如下的：
```gcc
    0x0021 ---->  0x0035   ---> 该地址的一维数组或者指针内存数值
    0x0025 ---->  0x0085   ---> ..
                  ...
    其中p指针的值为0x0021，通过p++来进行指针的移动，从而以一维数组或者指针为单位
    进行跳跃。

    此时：
        *p  表示操作0x0021中的值，0x0035，是一个一维指针
        **p 表示操作0x0035中的值，**p = 3； 是合法的。
```

###### 2.2.2.2 二维数组
此时双重指针的地址指向如下：
```gcc
    0x0021 ---> 8 1 2 3 4
                0 0 0 0 0
    即*p的指针直接为数组的首地址0x0021==&array[0][0]值，此时如果再进行解引用，
    那么结果为：
        对0x8的地址进行操作，发生Segment Fault.
```


### 3 指针
> 指向指针的指针/指向数组的指针
#### 3.1 类型
二级指针——指向指针的指针
```gcc
    int **p = NULL;
```
指向数组的指针
```gcc
    int array[4][3] = {...};
    int (*p)[3] = array;
```
指向函数的指针
```gcc
    typedef int (*p2)(...);
```
#### 3.2 步长图
```gcc
    声明                    基本类型            步长
    int *p0                 int                 int

    int **p1                int*                指针

    int *array[4]           数组                int *

    int array1[3][4]        数组                int

    int (*p2)[4]            int a[4]            4*int，很重要

    int (*p3)(...)          函数                无

    int* p4(...)            函数                无
```
