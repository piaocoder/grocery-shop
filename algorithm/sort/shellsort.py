#!/usr/bin/env python
#coding:utf-8
##
# @file shellsort.py
# @brief    shell sort simple test
#       分析：
#           1，本质上，一种比较类-非线性-插入类-改进的插入-排序
#           2，什么？你说插入排序最优和最差的区别好大？难道说？
#               最优：
#                   整个队列基本有序，此时O(n)
#               最差：
#                   O(n*n)
#           3，最优时的特征
#               越是基本有序，比较和移动的次数越小
#               n越小，O(n*n)越小哦（二分思维）
#           4，希尔希尔来临：
#               我就将n减小，一开始小小的
#               然后慢慢增加
#               最后进行最后一次完整的insert sort（n为列表全长）
#           5，如果step = 5，那么就有5列，对每一列进行插入排序
#               13 14 94 33 82
#               25 59 94 65 23
#               45 27 73 25 39
#               10
#               ==============
#               10 14 73 25 23
#               13 27 94 33 39
#               25 59 94 65 82
#               45
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


def shellSort(list1):
    """shellSort

    :param list1:
    """
    list_len = len(list1)
    step = int(round(list_len / 2))

    while step > 0:
        # 注意，下面的排序思路完全仿照insertsort中的写法
        for i in range(step, list_len):
            # 第i/step列的第二位元素，之后变为第i/step + 1列，...
            temp = list1[i]
            index = i
            for j in range(i - step, - 1, -step):
                if list1[j] > temp:
                    list1[j + step] = list1[j]
                    index = j
                else:
                    break
            list1[index] = temp

        step = int(round(step / 2))

    return list1


if __name__ == '__main__':
    list1 = [25353, 535, 53, 5, 696, 2953, 502, 55, 332, 222]
    print '原始列表：'
    displayList(list1)
    shellSort(list1)
    print '排序后的列表：'
    displayList(list1)
    pass
