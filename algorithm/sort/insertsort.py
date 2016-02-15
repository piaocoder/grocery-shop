#!/usr/bin/env python
#coding:utf-8
##
# @file insertsort.py
# @brief    insert sort simple test
#       分析：
#           1，本质上，一种比较类-非线性-插入类-排序
#           2，民主自由的制度，不到最后，谁都不能确定村长是谁！(其实吧，
#               结果还不是一样，选择的方向不同而已)
#           3，来来来，一个个来，大家排好队，之后不断的更改顺序（对于任何
#               一个新的未排序元素，有选择的插入已排序队列中）
#           4，你，就是你，你身高多少？185？
#               比SB1高啊.....
#                   SB1，你往后面走一步，index=SB1之前的位置
#               比SB2高啊....
#                   SB2，你往后走一步，index=SB2之前的位置
#               嘿嘿，没有SB3高！
#                   滚到index里面站着吧
#           5，插入排序的最优性能：
#               基本有序，此时做的操作基本为0
#               选择排序就不是咯，还是的选择出最大值
#               交换排序也是，但是吧
#               所以，希尔排序才会以插入排序为基础
# @author unlessbamboo
# @version 1.0
# @date 2016-02-15


def insertSort(list1):
    """insertSort

    :param list1:
    """
    list_len = len(list1)

    # 1，从改列的第二个元素开始
    for i in range(1, list_len):
        # 2，记住当前欲插入的元素为tmp
        tmp = list1[i]
        # 3，空闲位置
        index = i
        # 4，从前面的已排序序列的尾部开始往前遍历，递减比较
        for j in range(i - 1, -1, -1):
            if tmp < list1[j]:
                list1[j + 1] = list1[j]
                index = j
            else:
                break

        list1[index] = tmp

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
    insertSort(list1)
    print '排序后的列表：'
    displayList(list1)
    pass
