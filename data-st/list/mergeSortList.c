#include <stdio.h>
#include <stdlib.h>
/**
 * @file mergeSortList.c
 * @brief   merge two sort list
 * @author unlessbamboo
 * @version 1.0
 * @date 2016-02-14
 */

typedef struct mylist mylist_t;
struct mylist{
    int             num;
    struct mylist  *next;
};


/**
 * @brief   mergeUnrecursiveList 
 *      分析：
 *      1，判断是否为空，任意一个链表为空，返回非空链表
 *      2，定义链表头curlist1,curlist2
 *      3，寻找首个链表节点：
 *          if list1->num > list2->num:
 *              head = list2;
 *              curlist2 = list2->next;
 *          else
 *              head = list1;
 *              curlist1 = list1->next;
 *          curhead = head;
 *      4，curlist1以及curlist2都不为空:
 *          if curlist1->num > curlist2->num:
 *              curhead->next = curlist2;
 *              curlist2 = curlist2->next;
 *          else
 *              curhead->next = curlist1;
 *              curlist1 = curlist1->next;
 *          curhead = curhead->next;
 *          loop
 *      5，合并其余项
 *          if curlist1:
 *              curhead->next = curlist1;
 *          else if curlist2:
 *              curhead->next = curlist2;
 *      6，返回结果
 *          return head;
 *      
 *
 * @param   list1
 * @param   list2
 */
mylist_t* mergeUnrecursiveList(mylist_t *list1, mylist_t *list2)
{
    mylist_t            *head, *curhead,*curlist1,*curlist2;

    curlist1 = list1;
    curlist2 = list2;

    // first node
    if (curlist1->num > curlist2->num) {
        head = curlist2;
        curlist2 = curlist2->next; 
    } else {
        head = curlist1;
        curlist1 = curlist1->next; 
    }
    curhead = head;
    curhead->next = NULL;

    // loop
    while (curlist1 && curlist2) {
        if (curlist1->num > curlist2->num) {
            curhead->next = curlist2;
            curlist2 = curlist2->next;
        } else {
            curhead->next = curlist1;
            curlist1 = curlist1->next;
        }
        curhead = curhead->next;
    }

    // merge remain list
    curhead->next = curlist1 ? curlist1 : curlist2;

    return head;
}


/**
 * @brief   mergeRecursiveList 
 *      分析：
 *          1，如果list1或者list2为空，返回另外一个非空链表
 *          2，判断，根据分治策略，任何小元素作为最终链表在当前阶段的尾部
 *              if list1->num < list2->num:
 *                  list1->next = mergeRecursiveList(list1->next, list2);
 *                  returnn list1;
 *              else
 *                  list2->next = mergeRecursiveList(list2->next, list1);
 *                  return list2;
 *
 * @param   list1
 * @param   list2
 *
 * @return  
 */
mylist_t* mergeRecursiveList(mylist_t *list1, mylist_t *list2)
{
    if (NULL == list1) return list1;
    if (NULL == list2) return list2;

    // locate tail
    if (list1->num < list2->num) {
        list1->next = mergeRecursiveList(list1->next, list2);
        return list1;
    } else {
        list2->next = mergeRecursiveList(list2->next, list1);
        return list2;
    }
}
