#!/usr/bin/env python
#coding:utf-8
##
# @file heapsort.py
# @brief    heap sort simple test（神奇的优先队列）
#       分析
#           1，本质上，一种比较类-非线性-选择类-排序
#           2，小游戏，从我们这些天才中选择top k的天才，好不，美女们!
#           3，近似完全二叉树：
#               堆性质：
#                   ki <= k2i 并且 ki <= k2i + 1
#                       或者
#                   ki >= k2i 并且 ki >= k2i + 1
#                   其中(1 <= i <= n/2)
#
#               二叉堆性质：
#                   value(父节点) >= value(子节点)
#                   任何一个子树都是一个二叉堆
#
#           4，问题来了，如何将n个人构建一个堆结构？
#               将所有子树调整为堆结构（n/2, n/2-1, ..., 1）
#               此时的堆为大根堆，即所有的父节点均大于子节点
#               但是啊，不会top k啊
#
#           5，对大根堆进行排序操作:（最大堆的算法）
#               交换R[1]和R[n]，人工构建了一个非堆结构，重建堆R[1...n-1];
#               交换R[1]和R[n-1]，重建堆R[1...n-2]，有序堆R[n-1..n];
#               不断的作死，不断的修补，最终得到一个最小堆结构;
#               如果要得最大堆，交换R[n]和R[i]，重建堆R[i+1..n]，有序堆R[1..i];
#
#           为何是选择排序类别？
#               不断的自我作死，选择出最大的根节点放在合适的位置上
#
#           游戏开始，我是裁判：
#               你们，组一个大根堆!
#                   n秒后，来，最天才的，站我旁边
#               你们，剩余的n-1的SB，再组一个大根堆
#                   n秒后，来，最天才的，站在刚才最最天才的旁边
#               .....唉
#
# @author unlessbamboo
# @version 1.0
# @date 2016-02-15


def moveDown(list1, start, end):
    """moveDown：调整堆结构

    :param list1:
    :param start:heap min edges
    :param end:head max edges
    """
    # children node
    largest = 2 * start + 1
    while largest <= end:
        # 获取孩子的最大值（可能左、可能右）
        # 左孩子：2 * start + 1
        # 右孩子：2 * start + 2
        if (largest < end) and (list1[largest] < list1[largest + 1]):
            largest += 1

        # 判断孩子最大值是否大于parent
        if list1[largest] > list1[start]:
            list1[largest], list1[start] = list1[start], list1[largest]
            # 继续GO GO
            start = largest
            largest = 2 * start + 1
        else:
            return


def create_heapify(list1, list_len):
    """create_heapify:创建初始堆

    :param list1:
    :param list_len:
    """
    first = int(list_len / 2 - 1)
    for start in range(first, -1, -1):
        moveDown(list1, start, list_len - 1)


def heap_sort(list1):
    """heap_sort:sort

    :param list1:
    """
    list_len = len(list1)

    # 构造大根堆
    create_heapify(list1, list_len)

    # 堆排序
    for end in range(list_len - 1, 0, -1):
        list1[end], list1[0] = list1[0], list1[end]
        moveDown(list1, 0, end - 1)
        # displayList(list1)

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
    heap_sort(list1)
    print '排序后的列表：'
    displayList(list1)
    pass
