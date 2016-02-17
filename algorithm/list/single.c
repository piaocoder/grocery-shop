#include "single.h"
/**
 * @file single.c
 * @brief   链表的操作
 *      链接：http://wuchong.me/blog/2014/03/25/interview-link-questions/
 * @author unlessbamboo
 * @version 1.0
 * @date 2016-02-16
 */



inline node_t* createNode(int data)
{
    node_t          *tmp = NULL;

    tmp = (node_t*)malloc(sizeof(node_t));
    if (NULL == tmp) {
        return NULL;
    } else {
        tmp->data = data;
        tmp->next = NULL;
        return tmp;
    }
}


inline bool insertNode(node_t *head, node_t *cur)
{
    if (NULL == head) {
        return false;
    }

    head->next = cur;

    return true;
}


node_t* findPreNode(node_t *head, node_t *cur)
{
    node_t          *tmp = NULL;

    tmp = head;
    
    while (tmp->next) {
        if (tmp->next->data == cur->data) {
            return tmp;
        }

        tmp = tmp->next;
    }

    return NULL;
}


/**
 * @brief   deleteNode
 *      分析：
 *          使用"从无头单链表中删除节点"方式（狸猫换太子）
 *              --->删除下一个节点，将下一个节点的数据替换到当前节点
 *              从而实现O(1)性能
 *      条件：
 *          保证不能是尾部节点，不能为头结点（findPreNode原因）
 *
 * @param   head
 * @param   cur
 *
 * @return  
 */
bool deleteNode(node_t *head, node_t *cur)
{
    node_t              *tmp = NULL;

    if (NULL == cur) {
        return false;
    }

    // tail node
    if (NULL == cur->next) {
        tmp = findPreNode(head, cur);
        if (NULL == tmp) {
            return false;
        } else {
            tmp->next = cur->next;
            free(cur);
            return true; 
        }
    }

    // O(1)
    tmp = cur->next;
    cur->data = tmp->data;
    cur->next = tmp->next;
    free(tmp);
    return true;
}
 
/**
 * @brief   reverseByLoop 
 *      分析：
 *          使用pre/next/head指针，从头开始进行逆置操作
 *          逆置过程中存在两个链表（没办法，过渡阶段，人民要忍耐）
 *      图解（head为额外空闲节点）：
 *          head -> node1 -> node2 --> node3
 *          ================
 *          thead = node1
 *          ====
 *          tmp = thead; thead = thead->next;
 *          tmp->next = head->next;
 *          head->next = tmp;
 *
 *          ================
 *          thead = node2
 *          ====
 *          tmp = thead; thead = thead->next;
 *          tmp->next = head->next;
 *          head->next = tmp;
 *
 *      图解（head也是有用节点）
 *          node1 --> node2 --> node3 --> node4
 *          pre = NULL
 *          =================
 *          head = node1;
 *          =====
 *          next = head->next;
 *          head->next = pre;
 *          
 *          pre = head;
 *          head = next;
 *
 * @param   head
 * @param   cur
 *
 * @return  
 */
node_t* reverseByLoop(node_t *head, node_t *cur)
{
    node_t              *tmp = NULL, *thead = NULL, *next = NULL;

    if (NULL == head) {
        return NULL;
    }

    thead = head->next;
    while (thead) {
        tmp = thead;
        thead = thead->next;

        tmp->next = head->next;
        head->next = tmp;
    }

    return head;
}

/**
 * @brief   reverseByRecursion 
 *          递归方式，此方法用在head为有效节点的链表中更为合适
 *
 * @param   head
 * @param   cur
 *
 * return  
 */
node_t* reverseByRecursion(node_t *head, node_t *cur)
{
    node_t          *tmp = NULL;

    if (NULL == cur || cur->next == NULL) {
        // 整个递归结束
        head->next = cur;
        return cur;
    }

    tmp = reverseByRecursion(head, cur->next);

    // 此时cur后面的节点已经发生巨大的变化，仅仅需要
    // 将cur和cur->next发生替换即可
    cur->next->next = cur;
    cur->next = NULL;

    return tmp;
}

/**
 * @brief   theKthNode 
 *          获取链表的倒数第k个节点
 *      分析：
 *          在不知道单链表总体数目的前提下，正常方法获取获取链表总数，
 *          最后再从头开始，这样不好
 *      解决办法：
 *          类此TCP的流动窗口，之后整个窗口整体后移到结尾，此时
 *          窗口首元素就是了（So perfect, so depressed.）
 *
 * @param   head
 * @param   k
 *
 * @return  
 */
node_t* theKthNode(node_t *head, int k)
{
    node_t          *start, *end;
    int              i = k;

    if (k < 0) {
        return NULL;
    }

    // create a window
    start = end = head->next;
    for(; i>0 && end != NULL; i--) {
        end = end->next;
    }

    // k > len(list)
    if (i > 0) {
        return NULL;
    }

    // move window
    while (NULL != end) {
        end = end->next;
        start = start->next;
    }

    return start;
}

/**
 * @brief   theMiddleNode :获取链表的中间节点
 *      分析：
 *          在不知道单链表总长度的前提下，普遍方法就是获取链表长度，
 *          最后再从新开始遍历即可
 *      解决：
 *          仍旧使用窗口模式，但是窗口大小是不断递增的，从而产生如下
 *          喜剧性效果：
 *              A1-->n/2，B1 --> n/2 + step(n/2)*1 == n，刚好到达末尾
 *
 * @param   head
 *
 * @return  
 */
node_t* theMiddleNode(node_t *head)
{
    node_t          *start, *end;

    start = end = head->next;

    while (NULL != end && NULL != end->next) {
        start = start->next;
        end = end->next->next;
    }

    return start; 
}


/**
 * @brief   hasCircle :判断链表是否存在环？
 *      分析：
 *          正常情况下，必须二次遍历链表，对每一个节点进行循环判断
 *      解决：
 *          物理学问题，两人跑步，最终会遇上
 *      双指针：
 *          双指针解决方式非常棒
 *
 * @param   head
 *
 * @return  
 */
bool hasCircle(node_t *head)
{
    node_t          *slow *fast;
    node_t          *circle = NULL;

    while (NULL != fast && NULL != fast->next) {
        fast = fast->next->next;
        slow = slow->next;
        if (slow == fast) {
            circle = fast;
            return true;
        }
    }

    return false
}


/**
 * @brief   findLoopPort :发现环入口点
 *      分析：
 *          1，环入口：
 *              1-->2 -->3 --->4 --->5 -->6
 *                             |          |
 *                             |9<-- 8<-- 7 
 *              这里4是入口点
 *      解决办法：
 *          a）安装环判断算法，先然p1/p2走到重合点M，p2每一次两步
 *          b）p2从链表头开始，每次一步，p1p2递增往前，最终会在4处回合
 *
 *      原因：
 *          len[1..4] = a
 *          len[4..M] = b
 *          len[4..4] = L（环长度）
 *          
 *          可得：
 *          a + b = n = a + b + k*L = 2*n
 *          推出：
 *              k*L = a+b = n
 *              即: a = (k*L - b)，L-b为M点到4的步数
 *                                        
 * @param   head
 *
 * @return  
 */
node_t* findLoopPort(node_t *head)
{
    node_t          *fast, *slow, *cur;

    if (NULL == head) {
        return NULL;
    }

    cur = head->next;
    if (NULL == cur && NULL == cur->next) {
        return NULL;
    }

    fast = slow = cur;

    // 获取重合点M
    while (NULL != fast && NULL != fast->next) {
        fast = fast->next->next;
        slow = slow->next;
        if (fast == slow) {
            break;
        }
    }

    if (fast != slow) {
        return NULL;
    }

    // 重新开始
    fast = head;
    while (fast != slow) {
        fast = fast->next;
        slow = slow->next;
    }

    return fast;
}

/**
 * @brief   isIntersect :判断两个无环链表是否相交
 *      分析：
 *          思路1：
 *              正常处理逻辑，对于链表1中的每一个节点，遍历链表2，
 *              判断是否相等，O(n*n)
 *          思路2：
 *              使用hash，对链表1构造hash，遍历链表2，执行hash查找
 *              O(n1 + n2)，额外空间
 *          思路3：
 *              按照上面的环思想，人为制造环，将链表2的头部连接到链表
 *              1的尾部，此时判断是否存在环结构，如果存在，则说明有环结构
 *          思路4：
 *              思路3的反证法思路，如果list1和list2不相交，因为list1和list2
 *              无环，则只能出现下面请看：
 *                  ○→○→
 *                          →○→○→○
 *                  ○→○→
 *              不可能为：
 *                  ○→○→      ○→○→
 *                          →○→
 *                  ○→○→      ○→○→
 *              或者：
 *                  其他
 *
 *              因此，仅仅需要判断末尾节点是否相同即可
 *
 * @param   head1
 * @param   head2
 *
 * @return  
 */
bool isIntersect(node_t *head1, node_t *head2)
{
    node_t              *t1, *t2;

    if (NULL == head1 || NULL == head2) {
        return false;
    }

    t1 = head1->next;
    t2 = head2->next;

    if (NULL == t1 || NULL == t2) {
        return false;
    }

    while (NULL != t1->next) {
        t1 = t1->next;
    }
    while (NULL != t2->next) {
        t2 = t2->next;
    }

    if (t1 == t2) {
        return true;
    } else {
        return false;
    }
}
