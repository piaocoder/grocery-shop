#!/usr/bin/env python
#coding:utf8
##
# @file generate-fife-test.py
# @brief    生成器的管道测试，当前生成器的数据来源于上一个生成器的输出
# @author unlessbamboo
# @version 1.0
# @date 2016-03-10


def genFind(fileList):
    """genFind

    :param filename:
    """
    for filename in fileList:
        f = open(filename)
        yield f
        f.close()


def genConcatenate(iobj):
    """genConcatenate

    :param iobj: 一个迭代对象，该对象中的每一个元素又是一个可迭代对象
    @替代操作：itertools中的chain函数
    """
    # 文件迭代
    for it in iobj:
        print '============================================'
        # 每一个文件中的行迭代，
        # 相当于python3中的yield from it用法
        for subit in it:
            yield subit


if __name__ == '__main__':
    fileObj = genFind(['/etc/passwd', '/etc/group'])
    chainObj = genConcatenate(fileObj)
    for line in chainObj:
        print line,
