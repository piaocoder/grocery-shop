#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "single.h"
/**
 * @file superOperator.c
 * @brief   链表的各种操作集锦
 * @author unlessbamboo
 * @version 1.0
 * @date 2016-02-16
 */


/**
 * @brief   deleteRandomNode:以O(1)方式链表中的当前节点，
 *          没有preNode的前提下、不是双链表的前提下
 *      解决：
 *          使用"从无头单链表中删除节点"：下一节点覆盖当前节点，删除下一个节点
 *          保证当前节点不是尾节点
 *
 * @param   cur
 */
void deleteRandomNode(node_t *cur)
{
    node_t          *pnode = NULL;
    
    assert(cur != NULL);
    assert(cur->next != NULL);

    pnode = cur->next;
    cur->data = pnode->data;
    cur->next = pnode->next;

    free(pnode);
    pnode = NULL;
}


int main(int argc, char **argv)
{
    deleteRandomNode(node);
    return 0;
}
