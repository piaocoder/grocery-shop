---
    Macro
---


### 1 Introduction
> 参考typeof.md文档中的信息
一些常用的，好玩的宏定义，例如下面说的offsetof，以及调试打印宏


### 2 定义


### 3 offsetof和container\_of
offsetof——用来判断结构体成员的偏移位置，使用虚拟0地址方式;
container\_of——根据成员的地址获取结构体的地址信息；
#### 3.1 offsetof
```gcc
    // 将虚拟地址0强制转化为指针type*，让编译器得到所需的偏移量值
    #define offsetof(type, member) (size_t)&( ((type*)0)->member )
```

#### 3.2 container\_of
功能：获取ptr和member名字获取整个结构体的内存地址信息
```gcc
    // ptr为成员变量的指针，type为结构体类型，member为成员变量名字
    #define container_of(ptr, type, member) ({ \
         const typeof( ((type *)0)->member ) *__mptr = (ptr); \
         (type *)( (char *)__mptr - offsetof(type,member) );})

    /*
        第一部分：定义一个member指针类型的指针变量__mptr
        第二部分：__mptr - member偏移量 == 结构体的内存地址
    */
```

