#!/usr/bin/env python
#coding:utf-8
##
# @file mergeSortList.py
# @brief    merge two sort list
# @author unlessbamboo
# @version 0.1
# @date 2016-02-14


def mergeUnrecurseList(list1, list2):
    """mergeUnrecurseList:unrecurse merge two list, return list1
    分析：
    1，判断是否为空，任意一个链表为空，返回非空链表
    2，遍历list1, lhead1和lhead2分别指向链表头 :
        如果curlist1.data小于等于curlist2.data，list2继续往后走
        如果curlist1.data大于curlist2.data：
            a）判断curlist2和lhead2之间是否存在其他节点：
                list1[curlist1-1]

    :param list1:
    :param list2:
    """

