/**
 * @file py-test.c
 * @brief   使用C制作python扩展模块包：
 *          1,注意Python.h头文件必须放在最前面，不然可能会出现一些
 *              warning信息
 * @author unlessbamboo
 * @version 1.0
 * @date 2016-03-03
 */

// C代码调，用上面的add函数
#include "Python.h"
#include <stdio.h>
#include <stdlib.h>


// 初始化Python
int main(int argc, char** argv)     
{
    // 在使用Python系统前，必须使用Py_Initialize对其
    // 进行初始化。它会载入Python的内建模块并添加系统路     
    // 是否初始化成功需要使用Py_IsInitialized。

    PyObject *pName, *pModule, *pDict, *pFunc, *pArgs, *pRetVal;

    Py_Initialize();     
    if ( !Py_IsInitialized() )         
        return -1;

    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append('./')");

    // 载入名为pytest的脚本(注意：不是pytest.py)
    pName = PyString_FromString("pytest");
    pModule = PyImport_Import(pName);
    if ( !pModule ) 
    {
        printf("can't find pytest.py");
        getchar();
        return -1;
    }
    pDict = PyModule_GetDict(pModule);
    if ( !pDict )         
    {
        return -1;
    }

    // 找出函数名为add的函数
    pFunc = PyDict_GetItemString(pDict, "add");
    if ( !pFunc || !PyCallable_Check(pFunc) )         
    {
        printf("can't find function [add]");
        getchar();
        return -1;
    }

    // 参数进栈
    pArgs = PyTuple_New(2);

    // PyObject* Py_BuildValue(char *format, ...)
    // 把C++的变量转换成一个Python对象。当需要从
    // C++传递变量到Python时，就会使用这个函数。此函数
    // 有点类似C的printf，但格式不同。常用的格式有
    // s 表示字符串，
    // i 表示整型变量，
    // f 表示浮点数，
    // O 表示一个Python对象。b=f(a) 0.1-0.01=0.09

    PyTuple_SetItem(pArgs, 0, Py_BuildValue("i",3)); 
    PyTuple_SetItem(pArgs, 1, Py_BuildValue("i",4)); 

    // 调用Python函数
    pRetVal = PyObject_CallObject(pFunc, pArgs);
    printf("function return value : %ld\r\n", PyInt_AsLong(pRetVal));

    Py_DECREF(pName);
    Py_DECREF(pArgs);
    Py_DECREF(pModule);
    Py_DECREF(pRetVal);

    // 关闭Python
    Py_Finalize();
    return 0;
}
