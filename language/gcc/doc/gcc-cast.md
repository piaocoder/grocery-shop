---
title: 类型转换和运算符  
date: 2016-09-03 21:00:00  
tags: c  
---

欢迎来到狂想的个人实验室。  
github：[unlessbamboo](https://github.com/unlessbamboo)


### Introduction
- 数字运算和类型转换
- 基本数据类型范围
- 空的含义
- 运算符优先级
- 位运算


### 1 数字运算和类型转换
> 首先，我声明：这是一段关于过去的记忆，不在意黑白，只思经历以及那份悸动--2014-08-01 笔记重新记录摘要
 
> C语言中的强制运算时很暴力的，不像C++，存在专门的修饰符（这个，其实C++也一样吧）
#### 1.1 社会阶层
    float(旁系) --->  double(顶层)
                   ^
                   |
    long  --->   unsigned long
      ^            ^
      |            |
    int   --->   unsigned int
      ^            ^
      |            |
    char/short--> unsigned char/unsigned short

- 处于社会阶层的越顶端，该数据类型的精度越高，所能表示的数据范围越大；
- 数据类型的自动转换规律：底层->高层，旁系->高层
- 遵循的逻辑：某个Monkey要保证数据的最有效性，另见《C Primer Plus》106页
#### 1.2 理解数字运算
这是一个数字的世界，数字世界的本质是依托一个个的元器件，所有的操作最终都归结
为0/1的操作，底层编辑器开发者对于所有数学运算的统一处理顺序为：

> 任何类型数---> 实体整数 ---> 更高等级精度数 ---> +/-/乘除 ---> 自动转换结果

例子：
``` gcc
    int ret;
    ret = 10 + 'a' + 6*3.000;
    // char自动转换为更高等级精度int
    ret == 10 + 97 + 6*3.000;
    ret == 107 + 18.000;
    ret == 125.000 = 125

    int ret2, b=6;
    // int自动转化为更高等级精度unsigned int
    ret2 = (unsigned int)b + (-20);
    ret2 == 6 + 4294967296 - 20;
    ret2 == 4297967282 == -14;
```
#### 1.3 常见类型转换
- 位数精度转换，低精度向高精度转换
- 赋值表达式中：右边服从左边
- 函数参数：实参必须转为行参


### 2 类型范围
> 一个人的社会阶层代表来其所能处理的能力
> 我去，什么鬼？bamboo当时在想什么呢？这么哲学化--2016-08-30

short/char          范围：-128~0~127
unsigned char       范围：0~255
int                 范围：-2147483648~0~2147483647，在某些古老的传说中：-32768~0~32767
unsigned int        范围：0~4294967295
long                范围：-2^63~0~2^63-1
float               指数范围：-2^128~0~2^128-1，精度范围：由尾数决定，2^23=8388608，所以范围为6～7位
double              符号为：1,指数位：11，有效位：52，其他参考float

##### 2.1 超额负担
一旦某一个类型的数据赋予了当前阶层所能承受的能力范围，要么浴火重生（赋值给高等级的类型），要么死亡然后轮回
``` gcc
    char c=128;
    int  b=2147483649;
    // 最后c的值为-128，b的值为-2147483647
```
> 虽然不同阶层有不同的能力范围，但是存在奇迹的（强制类型转换以及合适的高级代理人）

##### 2.2 二进制运算
在很久很久以前，一群科学家为了让计算机能够通过加法操作完成减法/符号运算，发明了来“反码”
- 反码：原码除符号位以外的所有值反转
- 原码：见1.2中类型范围介绍
- 补码：原码取反+1，“补上一个1,作为遁掉的一，从此大道可成”

过程说明：
``` gcc
    // 1.0 反码时代
    1 - 1 = [0000 0001] + [1000 0001]
          == [0000 0001]反 + [1111 1110]反
          == [1111 1111]反
          == [1000 0000]原 == 这个值被约定为-128，固该算法出现问题
    // 2.0 补码时代
    // 不存在-0这个整型数（遁掉咯），发明了来补码概念（时钟）
    1 - 1 = [0000 0001] + [1000 0001]
          == [0000 0001]反 + [1111 1110]反
          == [0000 0001]补 + [1111 1111]补
          == [0000 0000]补
          == [0000 0000]原 == 0
```
例子：
``` gcc
    128 = 127 + 1 == [0111 1111] + [0000 0001]
                  == [0111 1111]补 + [0000 0001]补
                  == [1000 0000]补
                  == [1111 1111]反 == [1000 0000]原 == -128

    129 = 127 + 2 == [0111 1111] + [0000 0010]
                  == [1000 0001]补
                  == [1000 0000]反 = [1111 1111] = -127
```


### 3 "空"的意义
#### 3.1 空
- null是一个哲学意义上的概念，即空值；
- NULL则是null这个空概念的一个实现机制
- 0仅仅是约定俗成上对于NULL的赋值，但是有时候NULL并不一定等于0
```
    #define NULL 0
```

#### 3.2 True/False/NULL区别
True/False并非1/0的概念，虽然宏定义是如此，True/False是表示一种真/假的
概念。
在逻辑表达式中，True/False是编译器约定俗成的结果值，虽然一般为1/0。
```gcc
    int a=0;
    printf("%d-%d-%d\n", a, (1!=0), NULL);
```
输出结果为：0-1-0


### 4 运算符优先级
#### 4.1 优先级
``` text
    () -> []  .
    ! ++ -- ~ - (type) * & sizeof
    算术运算
    逻辑运算
    位运算
    赋值运算
```
常见的运算符模糊顺序常常是取地址运算符和解析运算符的使用：
``` gcc
    struct exam temp;
    struct exam *point;
    
    // 注意下面的优先级
    int ret = &temp.a;
    point = &temp;
    int *p = &point->a;
```


### 5 位运算
#### 5.1 异或
位在处理很多细节，特别是巧妙的数学运算上有很大的功效，另外还有存储转换。
##### 5.1.1 交换整数
``` gcc
    // 加减法，无需在意溢出
    void swap(int *a, int *b) {
        *a = *a + *b;
        *b = *a - *b;
        *a = *a - *b;
    }

    // 异或法，请确保a!=b
    void swap(int *a, int *b) {
        *a = (*b)^(*a);
        // (*b)^(*b)^(*a)任意值同某一个值异或两次，结果不变
        *b = (*b)^(*a);
        *a = (*b)^(*a);
    }
```

##### 5.1.2 位数的翻转
```gcc
    // 位运算不能用于float和double类型
    // 从右开始的第n位翻转
    exp = exp^(1 << n);
```

#### 5.2 与
&运算符是用途最广的位操作符，可以实现：位的复位/高N位的清0/某一位值的判断等等；

##### 5.2.1 存储后n位值
这种用法常常用于将十进制变为其他进制位的输出
```gcc
    // 将num转变为16进制输出
    void printHex(int num) 
    {
        char ch;

        for (int i=28; i>=0; i-=4) {
            int temp = num&(15);

            temp>9 ? (ch='A'+temp-10) : (ch='0'+temp);
            printf("%c", ch);
        }
        printf("\n");
    }
```

##### 5.2.2 判断次幂
```gcc
    // 判断n是否为2的次幂
    int ret, n=13;

    // 如果ret为0：则n为2的次幂，vice versa.
    ret = n&(n-1);
```


#### 5.3 或
或运算和与运算是互通的，关键看怎样操作。


#### 5.4 位运算例子
##### 5.4.1 标志位
位运算在标志位用法中极为广泛，利用左移操作和&操作，验证某个标志位字段
```gcc
    // flags的总位数不能小于maxsize，从右往左提取非1的位数对应的输出
    for (i=0; i< maxsize; i++) {
        if (flags & (1 << i)) {
            get values;
        }
    }
```

##### 5.4.2 复杂标志位
对于上节的例子，仅仅适用于少量的标志位设置，如果标志位过多，该如何解决？
```gcc
    // 获取bit低5位的标志位信息，并移动到该标志位处，例如bit为30，则移动到
    // 2^30，第30为标志位处；
    #define BIT(bit)        (1<<((bit)%32))

    // 0<=bit<=255
    // 获取以32为基的某一个标志位集，例如BIN(mask, 30)=mask[0]，第一个标志为集
    #define BIN(mask,bit)   (mask)[((bit)>>5)%4]

    // 将某一个标志为集mask[0]上的第n为置为1
    // SET(mask, 31) == (2^31 | mask[0])
    #define SET(mask,bit)   (BIN(mask,bit) |= BIT(bit))

    // 将某一为置为0,注意，&和~结合使用
    #define CLR(mask,bit)   (BIN(mask,bit) &= ~BIT(bit))

    // 判断某一个标志是否为1
    #define TEST(mask,bit)  (BIN(mask,bit) & BIT(bit))
```


#### 5.5 位运算的思考逻辑
对于所有的位运算问题，需要认真分析（采用归纳法），采用相应的策略：
> 分析问题--》能否使用位操作来解决？--》应该使用什么方法来解决？