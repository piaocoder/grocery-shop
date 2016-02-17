#!/usr/bin/env python
#coding:utf-8
##
# @file selectsort.py
# @brief    select sort simple test（抓重点，慢慢来，计划经济）
#       分析：
#           1，本质上，一种比较类-非线性时间-选择类-排序
#           2，首先，选出村支书，它最大，也许"最小"
#           3，其次，选出村长
#           4，注意，选举时，只要记住门牌号就行，一人一门牌嘛
#           5，.....，大家该干嘛干嘛去
# @author unlessbamboo
# @version 1.0
# @date 2016-02-15


def selectSortReverse(list1):
    """selectSortReverse:人民群众放在第一位，虽然最后人民群众还是lower

    :param list1:
    """
    list_len = len(list1)

    for i in range(0, list_len):
        minIndex = i
        for j in range(i, list_len):
            if list1[j] < list1[minIndex]:
                minIndex = j

        list1[minIndex], list1[i] = list1[i], list1[minIndex]

    return list1


def selectSort(list1):
    """selectSort:

    :param list1:source list1
    """
    list_len = len(list1)

    for i in range(0, list_len)[::-1]:
        maxIndex = i
        for j in range(0, i):
            if list1[j] > list1[maxIndex]:
                maxIndex = j

        list1[maxIndex], list1[i] = list1[i], list1[maxIndex]

    return list1


def displayList(list1):
    """displayList

    :param list1:
    """
    for value in list1:
        print value,
    print


if __name__ == '__main__':
    list1 = [25353, 535, 53, 5, 696, 2953, 502, 55, 332, 222]
    print '原始列表：'
    displayList(list1)
    selectSort(list1)
    print '排序后的列表：'
    displayList(list1)
    pass
