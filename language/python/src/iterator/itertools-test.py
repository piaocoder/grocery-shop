#!/usr/bin/env python
#coding:utf8
##
# @file itertools-test.py
# @brief    itertools工具对应的迭代器操作测试
# @author unlessbamboo
# @version 1.0
# @date 2016-03-10
import itertools


def count(num):
    """count

    :param num:
    :NOTE：这里使用到了闭合操作
    """
    max = 50
    while True:
        yield num
        # 打印该值，拥有理解下面调用函数的原理
        # print 'xxx:', num
        if num >= max:
            raise StopIteration
        num += 1


def liceTest(iobj):
    """liceTest：对迭代器或者生成器进行切片操作
        1,为何不能使用标准的切片操作？因为切片操作必须
            实现知道对象的长度，这是生成器和迭代器的优势
            也是他们最大的缺点；
        2,islice原理：
            逐层迭代，知道找到对应的切片索引元素，之后开始往前，
            对于前面的元素，丢弃

    :param iobj:
    """
    for x in itertools.islice(iobj, 10, 20):
        print x


def dropTest(iobj):
    """dropTest:排除迭代器或者生成器前面的元素
        1，从15开始计数
        2，如果后面又出现小于15的数，此时不会发生排除操作
        3，该方法常常用于排除配置文件中的前面的注释行

    :param iobj:
    """
    for x in itertools.dropwhile(lambda v: v < 15, iobj):
        print x


def premutationTest(listObj):
    """premutationTest：获取元祖中的所有可能排列组合并返回迭代器

    :param listObj:
    """
    for num in itertools.permutations(listObj):
        print num


if __name__ == '__main__':
    iterObj = count(0)
    liceTest(iterObj)
    print 'xxxxxxxxxxxxxxxxxxdropwhilexxxxxxxxxxxxxxxxxxx'
    dropTest(iterObj)
    print 'xxxxxxxxxxxxxxxxxxpremutationxxxxxxxxxxxxxxxxxx'
    premutationTest([3, 10, 5])
