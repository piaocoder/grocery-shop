---
可变参数
---


### 1 前言
可变参数--variable argument
#### 1.1 需求
某一个函数在多个地方广受欢迎，为了提升自身的影响力，其必须将自身
尽可能的通用化，回到人民大众中去，允许参数的数量是不确定的。

#### 1.2 解决办法
- 古老的方式：利用链表/数组/结构体来传递可变参数；
- 可变参数宏：利用...和\_\_VA\_ARGS\_\_来实现；
- 可变参数列表函数


### 2 古老的传说
> 如果要传递不同类型的数据，需要额外的增加类型长度说明，类似va_arg获取不同类型数据

利用链表来传递多个不确定的参数
```gcc
    // 其中type标识不同的数据类型，从而决定value中的有效数据长度
    typedef struct V_LIST { 
        int type;
        unsigned char value[max];
        V_LIST *next;
    };

    void parseListArg(V_LIST *header)
    {
        遍历链表；
        对每一个node的处理；
        善后处理；
    }
```

利用数组来传递多个不确定的参数
```gcc
    void parseArrayArg(V_LIST *array, int num)
    {
        for (int i=0; i<num; i++) {
            遍历数组
        }
    }
    
```


### 3 可变参数宏
> 见《C Primer Plus》453页
在宏定义参数列表中的最后参数为省略号，预定义宏VAARGS用于替换相关可变列表
```gcc
    // 调试日志，关于##，见宏的相关知识
    #define DEBUG(fmt, ...) printf(fmt, ## __VA_ARGS__)
```


### 4 可变参数函数
> 见《C Primer Plus》478页
#### 4.1 可变参数步骤
- 在函数原型中使用省略号
- 创建va_list变量
- 用宏va_start初始化va_list变量，即将参数列表复制到该变量中
- 用宏va_arg访问参数列表，每一次访问一个参数，参数类型由参数决定（重要）
- 如果必要，使用宏va_copy，拷贝其他va_list变量
- 用宏va_end完成某些清理工作

#### 4.2 获取参数
在获取可变参数列表中的参数时，有一个非常重要的问题：
    参数类型/参数个数

##### 4.2.1 方法1  
参数格式：参数个数，可变类型1, 可变参数值1, 可变类型2, 可变参数值2, ...
```gcc
    void phaseFunc(int num, ...)
    {
        va_list vl;
        va_start(vl, num);

        for (int i=0; i<num; i+=2) {
            V_TYPE t = va_arg(vl, int);
            switch (t) {
                // 根据类型再调用va_arg函数
                ...
            }
        }
    }
```

##### 4.2.2 方法2
参考printf中的fmt方法，解析fmt，然后再调用va_arg来获取相应的信息
