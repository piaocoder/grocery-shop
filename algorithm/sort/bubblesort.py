#!/usr/bin/env python
#coding:utf-8
##
# @file bubblesort.py
# @brief    bubble sort simple test(邻居好说话)
#       分析：
#           1，本质上，一种比较类-非线性时间-交换类-排序
#           2，哇，政策下来了...
#               我比你大，我们两得换换了;（仅仅和相邻元素进行对比）
#               走一步是一步哪管得了不熟的人；
#               一个个来，不要急（每次仅仅将当前最大数归位）;
#           3，性能：O(n*n)
# @author unlessbamboo
# @version 1.0
# @date 2016-02-15


def displayList(list1):
    """displayList

    :param list1:
    """
    for value in list1:
        print value,
    print


def bubbleSort(list1):
    """bubbleSort

    :param list1:source list1
    """
    list_len = len(list1)
    for i in range(list_len):
        j = list_len - i - 1
        for k in range(j):
            if list1[k] > list1[k + 1]:
                list1[k], list1[k + 1] = list1[k + 1], list1[k]


if __name__ == '__main__':
    list1 = [25353, 535, 53, 5, 696, 2953, 502, 55, 332, 222]
    print '原始列表：'
    displayList(list1)
    bubbleSort(list1)
    print '排序后的列表：'
    displayList(list1)
    pass
