#ifndef _SINGLE_LIST_H_
#define _SINGLE_LIST_H_

#if !defined(__bool_true_false_are_defined) && !defined(__cplusplus);
typedef int bool;
#define true 1
#define false 0 
#define __bool_true_false_are_defined
#endif          

typedef struct node node_t;
struct node{
    int          data;
    struct node *next;
};


inline node_t* createNode(int data);
inline bool insertNode(node_t *head, node_t *cur);
bool deleteNode(node_t *head, node_t *cur);
node_t* findPreNode(node_t *head, node_t *cur);

node_t* reverseByLoop(node_t *head, node_t *cur);
node_t* reverseByRecursion(node_t *head, node_t *cur);

node_t* theKthNode(node_t *head, int k);
node_t* theMiddleNode(node_t *head);

bool hasCircle(node_t *head);
node_t* findLoopPort(node_t *head);
bool isIntersect(node_t *head1, node_t *head2);

#endif
