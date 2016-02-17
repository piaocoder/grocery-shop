#!/usr/bin/env python
#coding:utf-8
##
# @file quicksort.py
# @brief    quick sort simple test.
#       分析：
#           1，本质上，比较类-非线性时间-交换类-二分法思维（分而治之）-排序
#           2，大哥，我们两一起将SB归为SB，NB归为NB，标准以我为参考（k = A[i]）
#           3，大哥，你先走，我等下将NB的人替换你哪里SB的人（交换A>k,B<k的两值）
#           4，大哥，革命会师之日就是你我相见之时（表示一次基准二分结束）
#
# @author unlessbamboo
# @version 1.0
# @date 2016-02-15


def qsort(list1, left, right):
    """qsort:quick sort

    :param list1:source list
    :param left:left index of list1 at current sort
    :param right:right index of list1 at current sort
    """
    # 革命会师，好久不见
    if left >= right:
        return list1

    k = list1[left]
    lp = left
    rp = right

    while lp < rp:
        # 必须大哥先走
        while rp > lp and list1[rp] >= k:
            rp -= 1

        # 小弟来换大哥的SB了
        while lp < rp and list1[lp] <= k:
            lp += 1

        list1[lp], list1[rp] = list1[rp], list1[lp]

    # 大哥，将我们脚下这笨蛋替换为一开始的标准
    list1[left], list1[lp] = list1[lp], list1[left]

    # 一个新的轮回，大哥，来世再见
    qsort(list1, left, lp - 1)
    qsort(list1, lp + 1, right)

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
    qsort(list1, 0, len(list1) - 1)
    print '排序后的列表：'
    displayList(list1)
    pass
