---
typedef的说明
---


## 1,Introduction
在了解typedef之前，请认真了解typedef和MACRO(例如define)的本质区别;  
理解typedef在代码中的真正含义（）


## 2,typedef和define的区别

### 2.1,区别
#### 2.1.1 typedef关键字
typedef本质上是一个gcc的关键字，一个存储关键字（auto,extern,mutable,static,register)，虽然其本身不能影响所修饰对象的存储特性；

#### 2.1.2 define宏
宏定义，用于简化C的代码，模块化以及复用思想的一种实现方式

#### 2.1.3 其他
-   执行时间不同
-   功能不同，见上
-   作用域，其中define没有作用域


### 2.2,例子
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


## 3,typedef的格式详解
> typedef是为一个指针或者变量类型的别名（alias）

对于如下语句：
```gcc
    typedef int (*FUNC1)(int, int);
```
### 3.1,普通的指针别名定义如下：
```gcc
        // 通用的：其中p1是一个用typedef定义的char类型的指针变量
        typedef char (*p1);
```
### 3.2,函数指针用法如下：
具体见函数指针文章的说明
```gcc
        // 1,首先func为一个指针
        // 2,其次int P2(int, int)是一个函数
        // 3,固func是一个指向函数的指针（函数指针）
        int (*func)(int, int);
```
### 3.3,最终结论：
FUNC1是一个指向函数int S(int, int)的指针的类型别名；
> FUNC1相当于类，func相当于对象实例


## 4,typedef用途
> 万事万物皆有其原始的出发点，所有人都是自私的
### 4.1,定义alias，以便同时声明多个对象
指针的用法最能说明这种用法的好处
``` gcc
    typedef char* pchar;
    pchar var1, var2, var3;
    char *var4, *var5, *var6;
```

### 4.2,作用域struct
其实就是1中介绍的alias用法，简化来struct的代码，增加可读性
```gcc
    typedef struct Test Test_t;
    struct Test {
        int a;
        Test_t  *next;
    };
    Test_t obj;
```

### 4.3,定义平台无关代码
类似宏的用法，尽可能的降低平台依赖，更容易更改代码
```gcc
    typedef long double REAL;

    REAL var1,...,varn;
```
此时，即使如果同样的代码在不同的平台运行，仅仅需要更改typedef
的定义即可，当然，可以让MACRO和typedef配合使用。


### 4.4,替换复杂的声明
替换某些过于复杂声明，提高代码的清晰度


## 5,例子
见src/macro/typedef.c中的例子说明
