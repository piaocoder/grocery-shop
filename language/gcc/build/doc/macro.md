---
Macro
---


### 1 Introduction
#### 1.1 定义
#### 1.2 语法
#### 1.3 typedef和宏
typedef是一个C关键字，是GCC扩展，见《GCC技术参考大全》79页。
- typedef和macro区别
- typedef格式
- typedef例子
#### 1.4 其他宏
offsetof、container\_of等等宏介绍


### 2 定义
Macro是C语言的扩展，预处理程序读出源代码，对内嵌的directive进行
响应，并生成源代码的修改版本----预处理过程


### 3 语法
#### 3.1 指示字
```gcc
    #define                         定义宏名字
    #if、#elif、#else、#endif       表达式判断
    #ifdef、#ifndef                 directive值判断
    #error、#warning                产生告警或者错误信息
    #include                        查找指示字列表并导入
    #line                           指出行号已经文件名
    #pragma                         指出编译程序或者平台
    #undef                          删除前面的directive定义
    ##                              连接两个指示字
```
#### 3.2 预定义宏
GCC预定义的宏集合
```gcc
    __FILE__                源文件
    __func__                函数名
    __LINE__                行号
    ......
```


### 4 typedef and Macro
#### 4.1 区别
##### 4.1.1 typedef关键字
typedef本质上是一个gcc的关键字，一个存储关键字
（auto,extern,mutable,static,register)，虽然其
本身不能影响所修饰对象的存储特性；
##### 4.1.2 define宏
宏定义，用于简化C的代码，模块化以及复用思想的一种实现方式
##### 4.1.3 分号
为何define中不设置分号？
```
    这个问题困扰来我好久，#define本身就是一种预处理替换机制，
    不是C语句，万一由某一个NB之人需要以分号结尾的宏呢？哈哈，
    所以，#define末尾不存在任何额外的信息，如果存在额外的信息，
    都会并入宏变量的值中了哦。
```
##### 4.1.4 其他
-   执行时间不同
-   功能不同，见上
-   作用域，其中define没有作用域
#####  4.1.5 例子
``` gcc
    // 同时定义两个变量或者宏
    typedef char* P1;
    #define P2  char*

    // 分别使用P1和P2来定义新的变量
    P1 var1, var2;
    P2 var3, var4;
```
上面的例子中，var3和var4语句会发生什么问题？上面的两行代码翻译之后变为：
``` gcc
    char *var1, *var2;
    // define
    char* var3, var4;
```
即define定义的宏仅仅做一个简单的代码替换而已。

#### 4.2 格式
> typedef是为一个指针或者变量类型的别名（alias）

对于如下语句：
```gcc
    typedef int (*FUNC1)(int, int);
```
##### 4.2.1 普通的指针别名
```gcc
        // 通用的：其中p1是一个用typedef定义的char类型的指针变量
        typedef char (*p1);
```
##### 4.2.2 函数指针
具体见函数指针文章的说明
```gcc
        // 1,首先func为一个指针
        // 2,其次int P2(int, int)是一个函数
        // 3,固func是一个指向函数的指针（函数指针）
        int (*func)(int, int);
```
##### 4.2.3 最终结论
FUNC1是一个指向函数int S(int, int)的指针的类型别名；
> FUNC1相当于类，func相当于对象实例

#### 4.3 typedef用途
> 万事万物皆有其原始的出发点，所有人都是自私的
##### 4.3.1 定义alias
以便同时声明多个对象，指针的用法最能说明这种用法的好处
``` gcc
    typedef char* pchar;
    pchar var1, var2, var3;
    char *var4, *var5, *var6;
```
##### 4.3.2 作用域
其实就是1中介绍的alias用法，简化来struct的代码，增加可读性
```gcc
    typedef struct Test Test_t;
    struct Test {
        int a;
        Test_t  *next;
    };
    Test_t obj;
```
##### 4.3.3 平台无关代码
类似宏的用法，尽可能的降低平台依赖，更容易更改代码
```gcc
    typedef long double REAL;

    REAL var1,...,varn;
```
此时，即使如果同样的代码在不同的平台运行，仅仅需要更改typedef
的定义即可，当然，可以让MACRO和typedef配合使用。

##### 4.3.4 替换复杂声明
替换某些过于复杂声明，提高代码的清晰度

#### 4.4 例子
见src/macro/typedef.c中的例子说明


### 5 其他宏
#### 5.1 offsetof
offsetof——用来判断结构体成员的偏移位置，使用虚拟0地址方式;
```gcc
    // 将虚拟地址0强制转化为指针type*，让编译器得到所需的偏移量值
    #define offsetof(type, member) (size_t)&( ((type*)0)->member )
```

#### 5.2 container\_of
container\_of——根据成员的地址获取结构体的地址信息；
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

